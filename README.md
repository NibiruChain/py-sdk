# Nibiru Python SDK                           <!-- omit in toc -->

> Interact with the Nibiru protocol using Python.

[![PyPI Version][pypi-image]][pypi-url]
[![][documentation-image]][documentation-url]
[![][discord-image]][discord-url]
[![][stars-image]][stars-url]

<!-- Badges: -->

[pypi-image]: https://img.shields.io/pypi/v/nibiru-py
[pypi-url]: https://pypi.org/project/nibiru-py/
[stars-image]: https://img.shields.io/github/stars/NibiruChain?style=social
[stars-url]: https://github.com/NibiruChain
[documentation-image]: https://readthedocs.org/projects/nibiru-py/badge/?version=latest
[documentation-url]: https://nibiru-py.readthedocs.io/en/latest/?badge=latest
[discord-image]: https://img.shields.io/discord/947911971515293759
[discord-url]: https://discord.gg/

The nibiru-py allows you to connect and trade with the Nibiru Protocol. It provides quick access to market data for storage, analysis, visualization, indicator development, algorithmic trading, strategy backtesting, bot programming, and related software engineering.

It is intended to be used by coders, developers, technically-skilled traders, data-scientists and financial analysts for building trading algorithms.

#### README Contents
- [Documentation Website](#documentation-website)
- [Quick Start](#quick-start)
- [Usage Instructions](#usage-instructions)
- [Development Guidelines](#development-guidelines)
  - [Python dependencies](#python-dependencies)
  - [Running the tests](#running-the-tests)
  - [Other dependencies](#other-dependencies)
  - [Generating types wth protobuf](#generating-types-wth-protobuf)
- [Linting](#linting)
- [Gotchas](#gotchas)

## Documentation Website

Documentation can be found here: [Nibiru-py documentation](https://nibiru-py.readthedocs.io/en/latest/index.html)

- Learn more about opening and managing your spot and perp positions [here](https://nibiru-py.readthedocs.io/en/latest/nibiru.sdks.tx.html#nibiru-sdks-tx-package)
- Learn about querying the chain using the Sdk [here](https://nibiru-py.readthedocs.io/en/latest/nibiru.clients.html#nibiru-clients-package)

## Quick Start

Installation

```bash
pip install nibiru-py
```

---

## Usage Instructions

The [examples directory](https://github.com/NibiruChain/nibiru-py/tree/master/examples) contains runnable examples that showcase how to use the package.
- Requires Python 3.9+
- Requires a running instance of the Nibiru blockchain


```bash
$ pipenv shell
$ pipenv install

# connecting to Nibiru Exchange API and create a new pool
$ python examples/chain_client/dex/create_pool.py

# sending a msg with bank transfer signs and posts a transaction to the Nibiru Chain
$ python examples/chain_client/msg_send.py
```

Upgrade `pip` to the latest version, if you see these warnings:
  ```
  WARNING: Value for scheme.platlib does not match. Please report this to <https://github.com/pypa/pip/issues/10151>
  WARNING: Additional context:   user = True   home = None   root = None   prefix = None
  ```

---

## Development Guidelines

### Python dependencies

#### 1 (option A). Install the `nibiru-py` package from source

  ```sh
  pipenv shell
  pipenv install --dev
  ```

Set up a `.env` file to set environment variables for the tests.
```sh
# Example configuration for the Nibiry Python SDK
HOST="..."
VALIDATOR_MNEMONIC="..."
ORACLE_MNEMONIC="..."
GRPC_PORT="..."
LCD_PORT="..."
CHAIN_ID="..."
NETWORK_INSECURE=true
```

There's currently a "devnet" running in GCP that the CI workflows use. You can find these secrets at [this notion page](https://www.notion.so/nibiru/Resources-and-Repo-Configs-b31aa8074a2b419d80b0c946ed5efab0) if you have access to it or contact @Unique-Divine or @matthiasmatt. 
This is useful so that you can run every part of the package code without needing to visit other repositories.

#### 1 (option B). Install the `nibiru-py` package with `pip`

  ```sh
  # from local
  # build and install
  pip install .

  # from local build
  pip uninstall nibiru-py
  pip install nibiru-py --no-index --find-links /path/to/nibiru/nibiru-py/dist

  # from pypi
  pip uninstall nibiru-py
  pip install nibiru-py
  ```

### Running the tests

Package tests are written `pytest`. To run and edit them, follow the instructions for installation from source and use `pipenv run pytest`. 

### Other dependencies

To run shell scripts and commands in the `Makefile`, you'll need to install the following tools depending on your operating system.

- **Ubuntu**
  ```bash
  sudo apt install python3.X-dev autoconf automake build-essential libffi-dev libtool pkg-config
  ```
- **macOS**
  ```bash
  brew install autoconf automake libtool
  ```
- **Fedora**
  ```bash
  sudo dnf install python3-devel autoconf automake gcc gcc-c++ libffi-devel libtool make pkgconfig
  ```

### Generating types wth protobuf 

The objective is to run `make proto-gen`, which simply executes `scripts/protocgen.sh`.

In order to do this, you'll need to install a few packages on your system.
```sh
python -m pip install --user grpcio-tools
pip install mypy-protobuf
```

If you get a permissions error such as 
```
rm: cannot remove 'proto/proto/epochs/query.proto': Permission denied
```
call `sudo chown -R [USER-NAME] proto` using the name of user directory. 
You can find the value for `[USER-NAME]` quickly by running `whoami`. In other words, this should work: 

```sh
sudo chown -R $(whoami) proto
```

You're done generating types once you've successfully called

```sh
make proto-gen
poetry build # equivalently, you can run `python -m build`
```

## Linting

Enable git hook which will perform linting before each commit:

```shell
pre-commit install
```

This will keep your code clean.


## Gotchas

The `protobuf` package must be version 3.20.x or lower. Otherwise, the following error appears at runtime.

```
nibiru/clients/__init__.py:1: in <module>
    from .dex import Dex  # noqa
nibiru/clients/dex.py:8: in <module>
    from nibiru.proto.dex.v1 import query_pb2 as dex_type
nibiru/proto/dex/v1/query_pb2.py:16: in <module>
    from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
../../../anaconda3/envs/divine/lib/python3.9/site-packages/google/api/annotations_pb2.py:30: in <module>
    from google.api import http_pb2 as google_dot_api_dot_http__pb2
../../../anaconda3/envs/divine/lib/python3.9/site-packages/google/api/http_pb2.py:48: in <module>
    _descriptor.FieldDescriptor(
../../../anaconda3/envs/divine/lib/python3.9/site-packages/google/protobuf/descriptor.py:560: in __new__
    _message.Message._CheckCalledFromGeneratedFile()
E   TypeError: Descriptors cannot not be created directly.
E   If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
E   If you cannot immediately regenerate your protos, some other possible workarounds are:
E    1. Downgrade the protobuf package to 3.20.x or lower.
E    2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).
E
E   More information: https://developers.google.com/protocol-buffers/docs/news/2022-05-06#python-updates
```