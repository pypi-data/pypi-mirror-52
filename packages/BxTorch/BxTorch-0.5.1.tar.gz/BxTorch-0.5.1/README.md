# BxTorch

BxTorch is a high-level library for large-scale machine learning in [PyTorch](https://pytorch.org).
It is engineered both to cut obsolete boilerplate code while preserving the flexibility of PyTorch to create just about any deep learning model.

## Installation

BxTorch is available on PyPi, so simply run the following command:

```bash
pip install bxtorch
```

The latest version of BxTorch is `1.0.0`. The package will install all required dependencies.

## Features

Generally, BxTorch provides an object-oriented approach to abstracting
PyTorch's API. The core design objective is to provide an API both as simple
and as extensible as possible. The goal of this library is to be able to iterate between different models easily instead of squeezing out milliseconds
where it is not required.

Still, being focused on large-scale machine learning, BxTorch aims to make it
as easy as possible working with large datasets. This includes out-of-the-box
multi-GPU support where the user *does not need to write a single line of
code*. Currently, BxTorch only provides means for running training/inference
on a single machine. In case this is insufficient, you might be better off
using PyTorch's `distributed` package directly.

It must be emphasized that BxTorch is not meant to be a wrapper for PyTorch as
Keras is for TensorFlow - it only provides *extensions*.

## Documentation

Examples of the usage of BxTorch can be found in the [docs folder](docs).
Method documentation is currently only available as [docstrings](bxtorch).

## License

BxTorch is licensed under the [MIT License](LICENSE).
