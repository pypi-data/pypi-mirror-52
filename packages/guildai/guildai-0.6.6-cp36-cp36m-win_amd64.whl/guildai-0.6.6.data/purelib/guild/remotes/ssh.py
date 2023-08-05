# Copyright 2017-2019 TensorHub, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division

import json
import os
import logging
import subprocess
import sys

import click
import yaml

from six.moves import shlex_quote as q

from guild import click_util
from guild import remote as remotelib
from guild import remote_util
from guild import run as runlib
from guild import util
from guild import var

from guild.commands import package_impl

from . import ssh_util

log = logging.getLogger("guild.remotes.ssh")

class SSHRemote(remotelib.Remote):

    def __init__(self, name, config):
        self.name = name
        self._host = config["host"]
        self.port = config.get("port")
        self.user = config.get("user")
        self.private_key = config.get("private-key")
        self.connect_timeout = config.get("connect-timeout")
        self.guild_home = self._init_guild_home(config)
        self.guild_env = config.get("guild-env")
        self.use_prerelease = config.get("use-prerelease", False)
        self.init = config.get("init")

    @property
    def host(self):
        return self._host

    @staticmethod
    def _init_guild_home(config):
        guild_home = config.get("guild-home")
        if guild_home is not None:
            return guild_home
        guild_env = config.get("guild-env")
        if guild_env is None:
            return ".guild"
        return util.strip_trailing_sep(guild_env) + "/.guild"

    def push(self, runs, delete=False):
        for run in runs:
            self._push_run(run, delete)

    def _push_run(self, run, delete):
        cmd = ["rsync", "-al"]
        if delete:
            cmd.append("--delete")
        if log.getEffectiveLevel() <= logging.DEBUG:
            cmd.append("-vvv")
        else:
            cmd.append("-v")
        src = run.path + "/"
        dest_path = "{}/runs/{}/".format(self.guild_home, run.id)
        dest = ssh_util.format_rsync_host_path(self.host, dest_path, self.user)
        cmd.extend([src, dest])
        cmd.extend(
            ssh_util.rsync_ssh_opts(
                remote_util.config_path(self.private_key),
                self.connect_timeout,
                self.port))
        log.info("Copying %s", run.id)
        log.debug("rsync cmd: %r", cmd)
        subprocess.check_call(cmd)

    def pull(self, runs, delete=False):
        for run in runs:
            self._pull_run(run, delete)

    def _pull_run(self, run, delete):
        src_path = "{}/runs/{}/".format(self.guild_home, run.id)
        src = ssh_util.format_rsync_host_path(self.host, src_path, self.user)
        dest = os.path.join(var.runs_dir(), run.id + "/")
        cmd = ["rsync"] + self._pull_rsync_opts(delete) + [src, dest]
        cmd.extend(
            ssh_util.rsync_ssh_opts(
                remote_util.config_path(self.private_key),
                self.connect_timeout,
                self.port))
        log.info("Copying %s", run.id)
        log.debug("rsync cmd: %r", cmd)
        subprocess.check_call(cmd)
        remote_util.set_remote_lock(run, self.name)

    @staticmethod
    def _pull_rsync_opts(delete):
        opts = [
            "-al",
            "--inplace",
            "--exclude", ".guild/job-packages",
            "--exclude", ".guild/LOCK*"]
        if delete:
            opts.append("--delete")
        if log.getEffectiveLevel() <= logging.DEBUG:
            opts.append("-vvv")
        else:
            opts.append("-v")
        return opts

    def start(self):
        raise remotelib.OperationNotSupported(
            "start is not supported for ssh remotes")

    def reinit(self):
        if not self.init:
            raise remotelib.OperationNotSupported(
                "init is not defined for this remote")
        self._ssh_cmd(self.init)

    def stop(self):
        raise remotelib.OperationNotSupported(
            "stop is not supported for ssh remotes")

    def status(self, verbose=False):
        ssh_util.ssh_ping(
            self.host,
            user=self.user,
            private_key=self.private_key,
            verbose=verbose,
            connect_timeout=self.connect_timeout,
            port=self.port)
        sys.stdout.write("%s (%s) is available\n" % (self.name, self.host))

    def run_op(self, opspec, flags, restart, no_wait, **opts):
        with util.TempDir(prefix="guild-remote-pkg-") as tmp:
            _build_package(tmp.path)
            remote_run_dir = self._init_remote_run(tmp.path, opspec, restart)
        self._start_op(remote_run_dir, opspec, flags, **opts)
        run_id = os.path.basename(remote_run_dir)
        if no_wait:
            return run_id
        try:
            self._watch_started_op(remote_run_dir)
        except KeyboardInterrupt:
            raise remotelib.RemoteProcessDetached(run_id)
        else:
            return run_id

    def _init_remote_run(self, package_dist_dir, opspec, restart):
        remote_run_dir = self._init_remote_run_dir(opspec, restart)
        self._copy_package_dist(package_dist_dir, remote_run_dir)
        self._install_job_package(remote_run_dir)
        return remote_run_dir

    def _init_remote_run_dir(self, opspec, restart_run_id):
        if restart_run_id:
            return self._init_remote_restart_run_dir(restart_run_id)
        else:
            return self._init_remote_new_run_dir(opspec)

    def _init_remote_restart_run_dir(self, remote_run_id):
        run_dir = os.path.join(self.guild_home, "runs", remote_run_id)
        cmd = (
            "set -e; "
            "test ! -e {run_dir}/.guild/LOCK || exit 3; "
            "touch {run_dir}/.guild/PENDING; "
            "echo \"$(date +%s)000000\" > {run_dir}/.guild/attrs/started; "
            "rm -rf {run_dir}/.guild/job-packages; "
            "mkdir {run_dir}/.guild/job-packages"
            .format(run_dir=run_dir)
        )
        log.info("Initializing remote run for restart")
        try:
            self._ssh_cmd(cmd)
        except remotelib.RemoteProcessError as e:
            if e.exit_status == 3:
                raise remotelib.OperationError("running", remote_run_id)
            raise
        else:
            return run_dir

    def _ssh_cmd(self, cmd):
        ssh_util.ssh_cmd(
            self.host, [cmd],
            user=self.user,
            private_key=remote_util.config_path(self.private_key),
            connect_timeout=self.connect_timeout,
            port=self.port)

    def _init_remote_new_run_dir(self, opspec):
        run_id = runlib.mkid()
        run_dir = os.path.join(self.guild_home, "runs", run_id)
        cmd = (
            "set -e; "
            "mkdir -p {run_dir}/.guild; "
            "touch {run_dir}/.guild/PENDING; "
            "mkdir {run_dir}/.guild/attrs; "
            "echo 'pending:? ? ? {opspec}' > {run_dir}/.guild/attrs/opref; "
            "echo \"$(date +%s)000000\" > {run_dir}/.guild/attrs/started; "
            "mkdir {run_dir}/.guild/job-packages"
            .format(run_dir=run_dir, opspec=opspec)
        )
        log.info("Initializing remote run")
        self._ssh_cmd(cmd)
        return run_dir

    def _copy_package_dist(self, package_dist_dir, remote_run_dir):
        src = package_dist_dir + "/"
        host_dest = "{}/.guild/job-packages/".format(remote_run_dir)
        log.info("Copying package")
        ssh_util.rsync_copy_to(
            src, self.host, host_dest,
            user=self.user,
            private_key=remote_util.config_path(self.private_key),
            port=self.port)

    def _install_job_package(self, remote_run_dir):
        cmd_lines = []
        cmd_lines.extend(self._env_activate_cmd_lines())
        cmd_lines.extend([
            "cd %s/.guild/job-packages" % remote_run_dir,
            "guild install %s --upgrade *.whl --target ." % self._pre_flag(),
        ])
        cmd = "; ".join(cmd_lines)
        log.info("Installing package and its dependencies")
        self._ssh_cmd(cmd)

    def _pre_flag(self):
        if self.use_prerelease:
            return "--pre"
        else:
            return ""

    def _start_op(self, remote_run_dir, opspec, flags, **opts):
        cmd_lines = ["set -e"]
        cmd_lines.extend(self._env_activate_cmd_lines())
        cmd_lines.append(
            "export PYTHONPATH=$(realpath {run_dir})/.guild/job-packages"
            ":$PYTHONPATH"
            .format(run_dir=remote_run_dir))
        cmd_lines.append(_remote_run_cmd(remote_run_dir, opspec, flags, **opts))
        cmd = "; ".join(cmd_lines)
        log.info("Starting remote operation")
        self._ssh_cmd(cmd)

    def _watch_started_op(self, remote_run_dir):
        cmd_lines = ["set -e"]
        cmd_lines.extend(self._env_activate_cmd_lines())
        cmd_lines.append(
            "NO_WATCHING_MSG=1 guild watch --pid {run_dir}/.guild/JOB"
            .format(run_dir=remote_run_dir))
        cmd = "; ".join(cmd_lines)
        log.debug("watching remote run")
        try:
            self._ssh_cmd(cmd)
        except remotelib.RemoteProcessError as e:
            if e.exit_status != 2:
                raise
            raise remotelib.RunFailed(remote_run_dir)

    def list_runs(self, verbose=False, **filters):
        opts = _list_runs_filter_opts(**filters)
        if verbose:
            opts.append("--verbose")
        self._guild_cmd("runs list", opts)

    def filtered_runs(self, **filters):
        cmd_lines = ["set -e"]
        cmd_lines.extend(self._env_activate_cmd_lines())
        opts = _filtered_runs_filter_opts(**filters)
        cmd_lines.append("guild runs list %s" % " ".join(opts))
        cmd = "; ".join(cmd_lines)
        out = self._ssh_output(cmd)
        if not out:
            data = []
        else:
            data = json.loads(out.decode())
            assert isinstance(data, list), (data, self.name)
        return [remotelib.RunProxy(run_data) for run_data in data]

    def _ssh_output(self, cmd):
        return ssh_util.ssh_output(
            self.host, [cmd],
            user=self.user,
            private_key=remote_util.config_path(self.private_key),
            connect_timeout=self.connect_timeout,
            port=self.port)

    def _env_activate_cmd_lines(self):
        if not self.guild_env:
            return []
        cwd = self.guild_env
        if cwd.endswith("/env"):
            cwd = cwd[:-4]
        return ["QUIET=1 source %s/bin/activate" % self.guild_env]

    def one_run(self, run_id_prefix, attrs):
        """Returns run matching id prefix as remote.RunProxy with attrs.

        Currently only supports attrs as ["flags"].
        """
        assert len(attrs) == 1 and attrs[0] == "flags", attrs
        cmd_lines = ["set -e"]
        cmd_lines.extend(self._env_activate_cmd_lines())
        cmd_lines.append(
            "guild runs info %s --flags --private-attrs"
            % q(run_id_prefix))
        cmd = "; ".join(cmd_lines)
        out = self._ssh_output(cmd)
        return remotelib.RunProxy(self._run_data_from_yaml(out))

    @staticmethod
    def _run_data_from_yaml(s):
        data = yaml.load(s)
        data["flags"] = data.get("flags") or {}
        return data

    def watch_run(self, **opts):
        self._guild_cmd("watch", _watch_run_args(**opts))

    def _guild_cmd(self, name, args, env=None):
        cmd_lines = ["set -e"]
        cmd_lines.extend(self._env_activate_cmd_lines())
        cmd_lines.extend(self._set_columns())
        if env:
            cmd_lines.extend(self._cmd_env(env))
        cmd_lines.append("guild %s %s" % (name, " ".join(args)))
        cmd = "; ".join(cmd_lines)
        self._ssh_cmd(cmd)

    @staticmethod
    def _set_columns():
        w, _h = click.get_terminal_size()
        return ["export COLUMNS=%i" % w]

    @staticmethod
    def _cmd_env(env):
        return [
            "export %s=%s" % (name, val)
            for name, val in sorted(env.items())
        ]

    def delete_runs(self, **opts):
        self._guild_cmd("runs delete", _delete_runs_args(**opts))

    def restore_runs(self, **opts):
        self._guild_cmd("runs restore", _restore_runs_args(**opts))

    def purge_runs(self, **opts):
        self._guild_cmd("runs purge", _purge_runs_args(**opts))

    def label_runs(self, **opts):
        self._guild_cmd("runs label", _label_runs_args(**opts))

    def run_info(self, **opts):
        self._guild_cmd("runs info", _run_info_args(**opts))

    def check(self, **opts):
        self._print_remote_info()
        self._guild_cmd("check", _check_args(**opts))

    def _print_remote_info(self):
        sys.stdout.write("remote:                    %s (ssh)\n" % self.name)
        sys.stdout.write("host:                      %s\n" % self.host)
        sys.stdout.flush()

    def stop_runs(self, **opts):
        self._guild_cmd("runs stop", _stop_runs_args(**opts))

    def list_files(self, **opts):
        self._guild_cmd("ls", _ls_args(**opts), {"NO_PATH_HEADER": "1"})

def _list_runs_filter_opts(deleted, all, more, **filters):
    opts = []
    if all:
        opts.append("--all")
    opts.extend(_runs_filter_args(**filters))
    if deleted:
        opts.append("--deleted")
    if more > 0:
        opts.append("-" + ("m" * more))
    return opts

def _filtered_runs_filter_opts(**filters):
    opts = _runs_filter_args(**filters)
    opts.append("--json")
    return opts

def _runs_filter_args(
        ops, labels, unlabeled, running, completed, error,
        terminated, pending, marked, unmarked, started):
    args = []
    if completed:
        args.append("-C")
    if error:
        args.append("-E")
    for label in labels:
        args.extend(["--label", q(label)])
    for op in ops:
        args.extend(["-o", op])
    if running:
        args.append("-R")
    if terminated:
        args.append("-T")
    if pending:
        args.append("-P")
    if unlabeled:
        args.append("-u")
    if marked:
        args.append("--marked")
    if unmarked:
        args.append("--unmarked")
    if started:
        args.append(["--started", started])
    return args

def _build_package(dist_dir):
    log.info("Building package")
    args = click_util.Args(
        dist_dir=dist_dir,
        upload=False,
        sign=False,
        identity=None,
        user=None,
        password=None,
        skip_existing=False,
        comment=None)
    package_impl.main(args)

def _remote_run_cmd(
        remote_run_dir, opspec, op_flags, label, batch_label,
        disable_plugins, gpus, no_gpus, force_flags,
        needed, stop_after, optimize, optimizer, opt_flags,
        minimize, maximize, random_seed, max_trials,
        init_trials):
    cmd = [
        "NO_WARN_RUNDIR=1",
        "guild", "run", q(opspec),
        "--run-dir", remote_run_dir,
        "--pidfile", "%s/.guild/JOB" % remote_run_dir,
        "--quiet",
        "--yes",
    ]
    if label:
        cmd.extend(["--label", q(label)])
    if batch_label:
        cmd.extend(["--batch-label", q(batch_label)])
    if disable_plugins:
        cmd.extend(["--disable_plugins", q(disable_plugins)])
    if gpus:
        cmd.extend(["--gpus", q(gpus)])
    if no_gpus:
        cmd.append("--no-gpus")
    if force_flags:
        cmd.append("--force-flags")
    if needed:
        cmd.append("--needed")
    if stop_after:
        cmd.extend(["--stop-after", stop_after])
    if optimize:
        cmd.append("--optimize")
    if optimizer:
        cmd.extend(["--optimizer", optimizer])
    for val in opt_flags:
        cmd.extend(["--opt-flag", val])
    if minimize:
        cmd.extend(["--minimize", minimize])
    if maximize:
        cmd.extend(["--maximize", maximize])
    if random_seed is not None:
        cmd.extend(["--random-seed", random_seed])
    if max_trials is not None:
        cmd.extend(["--max-trials", max_trials])
    if init_trials:
        cmd.append("--init-trials")
    cmd.extend([q(arg) for arg in op_flags])
    return " ".join(cmd)

def _watch_run_args(
        run, ops, pid, labels, unlabeled, marked, unmarked,
        started):
    if pid:
        # Ignore other opts if pid is specified
        return ["--pid", pid]
    args = []
    for op in ops:
        args.extend(["-o", q(op)])
    for label in labels:
        args.extend(["-l", q(label)])
    if unlabeled:
        args.append("-u")
    if marked:
        args.append("--marked")
    if unmarked:
        args.append("--unmarked")
    if started:
        args.extend(["--started", started])
    if run:
        args.append(run)
    return args

def _delete_runs_args(runs, permanent, yes, **filters):
    args = _runs_filter_args(**filters)
    if permanent:
        args.append("-p")
    if yes:
        args.append("-y")
    args.extend(runs)
    return args

def _run_info_args(
        run, files, all_files, env, deps, scalars, sourcecode,
        follow_links, output, page_output, **filters):
    args = _runs_filter_args(**filters)
    if files:
        args.append("-" + "f" * files)
    if all_files:
        args.append("-a")
    if env:
        args.append("-e")
    if deps:
        args.append("-d")
    if scalars:
        args.append("-S")
    if sourcecode:
        args.append("-s")
    if follow_links:
        args.append("-L")
    if output:
        args.append("-O")
    if page_output:
        args.append("-p")
    if run:
        args.append(run)
    return args

def _check_args(tensorflow, verbose, offline):
    args = []
    if tensorflow:
        args.append("--tensorflow")
    if verbose:
        args.append("-v")
    if offline:
        args.append("--offline")
    return args

def _stop_runs_args(
        runs, ops, labels, unlabeled, no_wait, marked, unmarked,
        started, yes):
    args = []
    for op in ops:
        args.extend(["-o", q(op)])
    for label in labels:
        args.extend(["-l", q(label)])
    if unlabeled:
        args.append("-u")
    if no_wait:
        args.append("-n")
    if yes:
        args.append("-y")
    if marked:
        args.append("--marked")
    if unmarked:
        args.append("--unmarked")
    if started:
        args.extend(["--selected", started])
    args.extend(runs)
    return args

def _restore_runs_args(runs, yes, **filters):
    args = _runs_filter_args(**filters)
    if yes:
        args.append("-y")
    args.extend(runs)
    return args

def _purge_runs_args(runs, yes, **filters):
    args = _runs_filter_args(**filters)
    if yes:
        args.append("-y")
    args.extend(runs)
    return args

def _label_runs_args(runs, label, clear, yes, **filters):
    args = _runs_filter_args(**filters)
    if yes:
        args.append("-y")
    if clear:
        args.append("-c")
    args.extend(runs)
    if label:
        args.append(q(label))
    return args

def _ls_args(run, all, follow_links, no_format, path, sourcecode,
             **filters):
    args = _runs_filter_args(**filters)
    if all:
        args.append("-a")
    if follow_links:
        args.append("-L")
    if no_format:
        args.append("-n")
    if path:
        args.append("-p")
    if sourcecode:
        args.append("-s")
    if run:
        args.append(run)
    return args
