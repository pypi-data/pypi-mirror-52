# Train Keras MLP example

Keras models can be trained simply by running them.

    >>> cd("examples/keras")

Lets run the `mnist_mlp.py` script:

    >>> run("guild run mnist_mlp.py -y --no-gpus epochs=1",
    ...     timeout=180, ignore=("WARNING", "Refreshing"))
    Limiting available GPUs (CUDA_VISIBLE_DEVICES) to: <none>
    Using TensorFlow backend...
    60000/60000 ...
    test_loss: ...
    test_acc: ...
    <exit 0>

Here's the run info, including files and scalars:

    >>> run("guild runs info --files --scalars")
    id: ...
    operation: mnist_mlp.py
    from: .../examples/keras
    status: completed
    started: ...
    stopped: ...
    marked: no
    label: epochs=1
    sourcecode_digest: 7bfd666a0adc81544179c315d69426ca
    run_dir: ...
    command: ...
    exit_status: 0
    pid:
    flags:
      batch_size: 128
      epochs: 1
      num_classes: 10
    scalars:
      acc: ... (step 0)
      loss: ... (step 0)
      sys/...
      val_acc: ... (step 0)
      val_loss: ... (step 0)
      acc: ... (step 1)
      loss: ... (step 1)
      val_acc: ... (step 1)
      val_loss: ... (step 1)
    files:
      events.out.tfevents...
    <exit 0>
