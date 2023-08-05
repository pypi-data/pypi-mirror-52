# Batch runs - skopt

These tests run each of the skopt based optimizers:

    - gp
    - forest
    - gbrt

We'll use the `noisy.py` script in the `optimizers` sample project.

    >>> project = Project(sample("projects", "optimizers"))

A helper to run an optimizer batch:

    >>> def run(optimizer, x, trials, opt_flags=None):
    ...     project.run(
    ...         "noisy.py",
    ...         flags={"x": x},
    ...         opt_flags=opt_flags,
    ...         optimizer=optimizer,
    ...         max_trials=trials,
    ...         simplify_trial_output=True)

## Bayesian with gaussian process

Range without an initial value:

    >>> run("gp", "[-2.0:2.0]", 3)
    Found 0 previous trial(s) for use in optimization
    Initialized trial ...
    Running trial: noisy.py ...
    x: ...
    loss: ...
    Found 1 previous trial(s) for use in optimization...
    Initialized trial ...
    Running trial: noisy.py ...
    x: ...
    loss: ...
    Found 2 previous trial(s) for use in optimization...
    Initialized trial ...
    Running trial: noisy.py ...
    x: ...
    loss: ...

Range with an initial value and opt flags:

    >>> run("gp", "[-2.0:2.0:0.1]", 2, {"kappa": 1.5, "xi": 0.2})
    Found 0 previous trial(s) for use in optimization
    Initialized trial (noise=0.1, x=0.1)
    Running trial: noisy.py (noise=0.1, x=0.1)
    x: 0.100000
    noise: 0.1
    loss: ...
    Found 1 previous trial(s) for use in optimization
    Initialized trial (noise=0.1, x=...)
    Running trial: noisy.py (noise=0.1, x=...)
    x: ...
    noise: 0.1
    loss: ...

Range with a null value:

    >>> run("gp", None, 2)
    ERROR: [guild] flags for batch (noise=0.1, x=null) do not contain
    any search dimension - quitting
    <exit 1>

Our trials:

    >>> project.print_runs(flags=True, status=True)
    noisy.py+gp  acq-func=gp_hedge kappa=1.96 noise=gaussian random-starts=0 xi=0.01  error
    noisy.py     noise=0.1 x=...                                                      completed
    noisy.py     noise=0.1 x=0.1                                                      completed
    noisy.py+gp  acq-func=gp_hedge kappa=1.5 noise=gaussian random-starts=0 xi=0.2    completed
    noisy.py     noise=0.1 x=...                                                      completed
    noisy.py     noise=0.1 x=...                                                      completed
    noisy.py     noise=0.1 x=...                                                      completed
    noisy.py+gp  acq-func=gp_hedge kappa=1.96 noise=gaussian random-starts=0 xi=0.01  completed

Cleanup for next tests:

    >>> project.delete_runs()
    Deleted 8 run(s)

## Forest

Range without an initial value:

    >>> run("forest", "[-2.0:2.0]", 3)
    Found 0 previous trial(s) for use in optimization
    Initialized trial ...
    Running trial: noisy.py ...
    x: ...
    loss: ...
    Found 1 previous trial(s) for use in optimization
    Initialized trial ...
    Running trial: noisy.py ...
    x: ...
    noise: 0.1
    loss: ...
    Found 2 previous trial(s) for use in optimization
    Initialized trial ...
    Running trial: noisy.py ...
    x: ...
    noise: 0.1
    loss: ...

Range with an initial value and opt flags:

    >>> run("forest", "[-2.0:2.0:0.3]", 2, {"kappa": 1.3, "xi": 0.3})
    Found 0 previous trial(s) for use in optimization
    Initialized trial (noise=0.1, x=0.3)
    Running trial: noisy.py (noise=0.1, x=0.3)
    x: 0.300000
    noise: 0.1
    loss: ...
    Found 1 previous trial(s) for use in optimization
    Initialized trial (noise=0.1, x=...)
    Running trial: noisy.py (noise=0.1, x=...)
    x: ...
    noise: 0.1
    loss: ...

Our trials:

    >>> project.print_runs(flags=True, status=True)
    noisy.py         noise=0.1 x=...                     completed
    noisy.py         noise=0.1 x=0.3                     completed
    noisy.py+forest  kappa=1.3 random-starts=0 xi=0.3    completed
    noisy.py         noise=0.1 x=...                     completed
    noisy.py         noise=0.1 x=...                     completed
    noisy.py         noise=0.1 x=...                     completed
    noisy.py+forest  kappa=1.96 random-starts=0 xi=0.01  completed

Cleanup for next tests:

    >>> project.delete_runs()
    Deleted 7 run(s)

## GBRT

Range without an initial value and an opt flag:

    >>> run("gbrt", "[-2.0:2.0]", 2, {"random-starts": 2})
    Found 0 previous trial(s) for use in optimization
    Initialized trial ...
    Running trial: noisy.py ...
    x: ...
    noise: 0.1
    loss: ...
    Found 1 previous trial(s) for use in optimization...
    Initialized trial ...
    Running trial: noisy.py ...
    x: ...
    noise: 0.1
    loss: ...

Range with an initial value and opt flags:

    >>> run("gbrt", "[-2.0:2.0:0.4]", 3, {"kappa": 1.4, "xi": 0.4})
    Found 0 previous trial(s) for use in optimization
    Initialized trial (noise=0.1, x=0.4)
    Running trial: noisy.py (noise=0.1, x=0.4)
    x: 0.400000
    noise: 0.1
    loss: ...
    Found 1 previous trial(s) for use in optimization...
    Initialized trial (noise=0.1, x=...)
    Running trial: noisy.py (noise=0.1, x=...)
    x: ...
    noise: 0.1
    loss: ...
    Found 2 previous trial(s) for use in optimization...
    Initialized trial (noise=0.1, x=...)
    Running trial: noisy.py (noise=0.1, x=...)
    x: ...
    noise: 0.1
    loss: ...

Our trials:

    >>> project.print_runs(flags=True, status=True)
    noisy.py       noise=0.1 x=...                     completed
    noisy.py       noise=0.1 x=...                     completed
    noisy.py       noise=0.1 x=0.4                     completed
    noisy.py+gbrt  kappa=1.4 random-starts=0 xi=0.4    completed
    noisy.py       noise=0.1 x=...                     completed
    noisy.py       noise=0.1 x=...                     completed
    noisy.py+gbrt  kappa=1.96 random-starts=2 xi=0.01  completed
