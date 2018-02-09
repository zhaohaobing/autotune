# autotune
Hyperparameter tuning on GPUs

[![Build Status](https://travis-ci.org/vzhong/autotune.svg?branch=master)](https://travis-ci.org/vzhong/autotune)

## Installation

```bash
pip install git+git://github.com/vzhong/autotune.git

# Or get it straight from PyPI

pip install autotune
```

## Usage

You can use the binary:

```bash
autotune -h
```

Or use it programmatically:

```python
from autotune.tuner import RandomSearch
from autotune.spec import Spec

config = Spec.load('myconf.json')
tuner = RandomSearch('myprog.bin', config)
tuner.tune(2, out='output')
```

where `myconf.json` looks something like:

```json
{
  "foo": [-1, 1],
  "bar": [2.0, 3.0]
}
```

This will run 2 commands `myprog.bin --foo $FOO --bar $BAR` where `$FOO` is an integer sampled between `-1` and `1` and `$BAR` is a float sampled between `2.0` and `3.0`.
You can pass in an optional parameter `name='nickname'`, which will add to the command `--nickname $HASH`, where `$HASH` is a hash of the specific parameters used for this command.
You can also pass in an optional parameter `gpu=True`, which will queue jobs onto available GPUs.
The command then becomes `CUDA_VISIBLE_DEVICES=$GPU myprog.bin --foo $FOO --bar $BAR --gpu 0`, where `$GPU` is a free GPU (e.g. no memory usage).
