# Source code digest

Guild generates a digest of soure code files so that any change to
source code is reflected as a change to the digest.

For our tests, we'll work with a dynamically modified project.

    >>> project_dir = mkdtemp()

## Baseline digest

Here's an initial Guild file that defined an operation `op` that does
nothing.

    >>> write(path(project_dir, "guild.yml"), """
    ...   op:
    ...     main: guild.pass
    ... """)

And a project to run operations on:

    >>> project = Project(project_dir)

Here's our current project layout:

    >>> find(project_dir)
    guild.yml

We can peek at the digest for this directory that Guild will generate
by using the `file_util.files_digest` function.

    >>> from guild.file_util import files_digest

    >>> files_digest(project_dir)
    '38eaef56aa526c84cb706bfa550f9f41'

Let's run `op` and examine the results.

    >>> run, _out = project.run_capture("op", run_dir=mkdtemp())

Here's the copied source:

    >>> find(run.guild_path("sourcecode"))
    guild.yml

Guild saves the source code digest in the run's `sourcecode_digest`
attribute:

    >>> run.get("sourcecode_digest")
    '38eaef56aa526c84cb706bfa550f9f41'

## New source code file

Let's now add a new file to our project. We'll add a text file that
Guild will treat as source code by default.

    >>> write(path(project_dir, "hello.py"), "print('hello')\n")

Here's our project directory:

    >>> find(project_dir)
    guild.yml
    hello.py

And our digest:

    >>> files_digest(project_dir)
    'd58df49c7f24c45cbab98a816c7ad50e'

Next we'll generate a new run:

    >>> run, _out = project.run_capture("op", run_dir=mkdtemp())

Our copied source code:

    >>> find(run.guild_path("sourcecode"))
    guild.yml
    hello.py

And the source code digest attribute:

    >>> run.get("sourcecode_digest")
    'd58df49c7f24c45cbab98a816c7ad50e'

## Modified source code file

Let's simulate a change to our source code file `hello.py`.

    >>> write(path(project_dir, "hello.py"), "print('hola')\n")

Our new project digest:

    >>> files_digest(project_dir)
    '3c0e4b7789ce7d04bd39fe7d39283100'

And our run:

    >>> run, _out = project.run_capture("op", run_dir=mkdtemp())

Copied source code:

    >>> find(run.guild_path("sourcecode"))
    guild.yml
    hello.py

Generated source code digest:

    >>> run.get("sourcecode_digest")
    '3c0e4b7789ce7d04bd39fe7d39283100'

## Disabled source code digest

We can disable source code digest generation by way of our Guild file.

Let's modify the project Guild file to disable source code digests.

    >>> write(path(project_dir, "guild.yml"), """
    ...   op:
    ...     main: guild.pass
    ...     sourcecode:
    ...       digest: off
    ... """)

Let's generate a new run:

    >>> run, out = project.run_capture("op", run_dir=mkdtemp())
    >>> print(out)
    sourcecode digest disabled for operation 'op' - skipping

The operation still copies source code:

    >>> find(run.guild_path("sourcecode"))
    guild.yml
    hello.py

However, it does not generate a source code digest:

    >>> print(run.get("sourcecode_digest"))
    None

We can alternatively disable digests at the model level:

    >>> write(path(project_dir, "guild.yml"), """
    ...   - model: m
    ...     operations:
    ...       op:
    ...         main: guild.pass
    ...     sourcecode:
    ...       digest: off
    ... """)

    >>> run, out = project.run_capture("m:op", run_dir=mkdtemp())
    >>> print(out)
    sourcecode digest disabled for model 'm' - skipping

    >>> print(run.get("sourcecode_digest"))
    None

However, the operation can override the model:

    >>> write(path(project_dir, "guild.yml"), """
    ...   - model: m
    ...     operations:
    ...       op:
    ...         main: guild.pass
    ...         sourcecode:
    ...           digest: on
    ...     sourcecode:
    ...       digest: off
    ... """)

    >>> run, _out = project.run_capture("m:op", run_dir=mkdtemp())

    >>> run.get("sourcecode_digest")
    'f1b6bf6fe35769b9a708f9073b125730'

And to confim the digest:

    >>> files_digest(project_dir)
    'f1b6bf6fe35769b9a708f9073b125730'
