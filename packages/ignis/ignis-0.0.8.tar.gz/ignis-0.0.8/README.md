# Intuitive library to help with training neural networks in PyTorch

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d418757720864208adf721433bd3d55d)](https://www.codacy.com/app/Catastropha/ignis)
[![Codacy Badge](https://api.codacy.com/project/badge/coverage/d418757720864208adf721433bd3d55d)](https://www.codacy.com/app/Catastropha/ignis)
[![Build Status](https://api.travis-ci.org/catastropha/ignis.svg?branch=master)](https://travis-ci.org/catastropha/ignis)
[![Downloads](https://pepy.tech/badge/ignis)](https://pepy.tech/project/ignis)
[![Version](https://img.shields.io/pypi/v/ignis.svg?style=flat)](https://pypi.org/project/ignis/#history)
![License](https://img.shields.io/pypi/l/ignis.svg?style=flat)

`ignis` is a high-level library that helps you write compact but full-featured training loops with metrics, early stops,
and model checkpoints for deep learning library [PyTorch](https://pytorch.org/).

You can extend `ignis` according to your own needs. You can implement custom functionalities by extending simple
abstract classes.

## Installation

1.  Install PyTorch. You can find it here: [PyTorch](https://pytorch.org/)
2.  `pip install ignis`

## Examples

You can find examples in `examples/` directory

You can also run examples: `python examples/iris.py`

You might want to `export PYTHONPATH=/path/to/this/directory`

## Contribute

1.  Implement new functionalities
2.  Improve code design
3.  Improve comments and readme
4.  Tests