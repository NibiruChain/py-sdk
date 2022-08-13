# Nibiru Python SDK - `nibiru-py`                           <!-- omit in toc -->

> Python-based client for interacting with the Nibiru blockchain.

<!-- Badges -->

[![Nibiru Test workflow][tests-badge]][tests-workflow]
[![PyPI Version][pypi-image]][pypi-url]
[![][documentation-image]][documentation-url]
[![][discord-badge]][discord-url]
[![][stars-image]][stars-url]
[![MIT license][license-badge]][license-link]

<!-- Badges links -->

<!-- pypi -->
[pypi-image]: https://img.shields.io/pypi/v/nibiru-py
[pypi-url]: https://pypi.org/project/nibiru-py/
[stars-image]: https://img.shields.io/github/stars/NibiruChain?style=social
[stars-url]: https://github.com/NibiruChain
[documentation-image]: https://readthedocs.org/projects/nibiru-py/badge/?version=latest
[documentation-url]: https://nibiru-py.readthedocs.io/en/latest/?badge=latest
[discord-badge]: https://img.shields.io/badge/Nibiru%20Chain-%237289DA.svg?style=&logo=discord&logoColor=white
[discord-url]: https://discord.gg/sgPw8ZYfpQ
[license-badge]: https://img.shields.io/badge/License-MIT-blue.svg
[license-link]: https://github.com/NibiruChain/nibiru-py/blob/master/LICENSE
[tests-badge]: https://github.com/NibiruChain/nibiru-py/actions/workflows/pytests.yml/badge.svg
[tests-workflow]: https://github.com/NibiruChain/nibiru-py/actions/workflows/pytests.yml

The `nibiru-py` package allows you to index, query, and send transactions on the Nibiru Blockchain using Python. It provides access to market data for analysis, visualization, indicator development, algorithmic trading, strategy backtesting, bot programming, and related software engineering.

The package is intended to be used by coders, developers, technically-skilled traders and  data-scientists for building trading algorithms.

#### README Contents

- [User Guidelines](#user-guidelines)
  - [Documentation Website](#documentation-website)
  - [Installation from `PyPI`](#installation-from-pypi)
- [Development Guidelines](#development-guidelines)
  - [Setting up a professional dev environment with `pyenv` and `poetry`](#setting-up-a-professional-dev-environment-with-pyenv-and-poetry)
    - [Pyenv for managing multiple Python interpreters](#pyenv-for-managing-multiple-python-interpreters)
  - [Installing `poetry` for dependency resolution and publishing packages](#installing-poetry-for-dependency-resolution-and-publishing-packages)
  - [Installing external dependencies](#installing-external-dependencies)
  - [Running tests](#running-tests)
      - [Setting environment variables](#setting-environment-variables)
      - [Running the tests with `poetry` + `pytest`](#running-the-tests-with-poetry--pytest)
      - [(option B). Install the `nibiru-py` package with `pip`](#option-b-install-the-nibiru-py-package-with-pip)
  - [Makefile and Protocol Buffers](#makefile-and-protocol-buffers)
    - [Other dependencies](#other-dependencies)
    - [Generating types wth protobuf](#generating-types-wth-protobuf)
  - [Linting](#linting)
  - [Gotchas](#gotchas)

# User Guidelines

## Documentation Website

Documentation can be found here: [Nibiru-py documentation](https://nibiru-py.readthedocs.io/en/latest/index.html)

- Learn more about opening and managing your spot and perp positions [here](https://nibiru-py.readthedocs.io/en/latest/nibiru.sdks.tx.html#nibiru-sdks-tx-package)
- Learn about querying the chain using the Sdk [here](https://nibiru-py.readthedocs.io/en/latest/nibiru.clients.html#nibiru-clients-package)

## Installation from `PyPI`

```sh
pip install nibiru-py  # requires Python 3.9
```

You may need to update `pip` to get this to run:

```sh
python -m pip install --upgrade pip
```

<!-- NOTE --------- Deperecating this section as the examples don't work.

## Usage Instructions

The [examples directory](https://github.com/NibiruChain/nibiru-py/tree/master/examples) contains runnable examples that showcase how to use the package.
- Requires Python 3.9+
- Requires a running instance of the Nibiru blockchain

```bash
$ pipenv shell
$ pipenv install
```

```sh
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
-->

---

# Development Guidelines

Our recommended setup is `pyenv` in combination with `poetry`.

- `pyenv` is a tool for installing and managing Python interpreters. This will let you seamlessly switch between Python versions.
- `poetry` is used for managing virtual environments, dependency resolution, package installations, package building, and package publishing.
- We assume you're on a Unix machine such as WSL2 Ubuntu, MacOS, or a common Linux distro.

Currently, `nibiru-py` is created with Python 3.9.13. It may be compatible with higher versions, but we only run end-to-end tests in 3.9.13.

## Setting up a professional dev environment with `pyenv` and `poetry`

### Pyenv for managing multiple Python interpreters

If you're on MacOS or a common Linux distro, you can install `pyenv` with brew.

```sh
brew install pyenv
```

You'll then need to add the following snippet to your shell config, e.g. your `.bash_profile`, `.bashrc`, or `.zshrc`.

```sh
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv init --path)"
```

After using `source` on your config or restarting the shell, you should have the `pyenv` root command.

The command use to install any version of python is `pyenv install`. Display additional info for this command with `pyenv install --help`.

```sh
pyenv install 3.9.13 # example for nibiru-py
```

Once you have a version installed, you can print out the versions on your machine with:

```sh
pyenv versions
```

```
# example output
  system
* 3.9.13 (set by /home/realu/.python-version)
  3.10.4
```

In this example, I have 2 different interpreters installed on my machine. The one with the `*` is currently set as my **global interpreter**. This is set manually using the `pyenv global` command.

```sh
pyenv global 3.10.4   # switches the global interpreter to 3.10.4
```

You can verify this works as expected using `python --version`. You may be familiar with using `python3` as the command instead of `python`. With `pyenv`, this is not necessary.

Additional usage and installation instructions can be found in the [pyenv repo](https://github.com/pyenv/pyenv).

## Installing `poetry` for dependency resolution and publishing packages

Reference: [Poetry docs](https://python-poetry.org/docs/)

Poetry can be installed with both `curl` and `pip`. We recommended using `curl` so that it will be global to your machine.

NOTE We highly, highly, highly recommend that you DO NOT use `brew` to install `poetry`.
If you use `brew`, it's going to install directly to your system, which prevents you from being able to leverage `pyenv` to seamlessly switch between Python interpreters.

```sh
# installation with pip: recommended option in tandem with pyenv
pip install poetry
```

```sh
# For UNIX systems - installation with curl 
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

After this installation command, add the `poetry` binary to the path in your shell config (if it's not done automatically).

```sh
export PATH=$PATH:$HOME/.poetry/bin
```

## Installing external dependencies

The `nibiru-py` project is defined by its `pyproject.toml`. At the root of the repo, simply call:

```sh
poetry install
```

This will resolve dependencies between each of the project's packages and install them into a virtual environment.

## Running tests

#### Setting environment variables

There's currently a "devnet" running in GCP that the CI workflows use. You can find these secrets at [this notion page](https://www.notion.so/nibiru/Resources-and-Repo-Configs-b31aa8074a2b419d80b0c946ed5efab0) if you have access to it or contact one of the `CODEOWNERS` (@Unique-Divine, @matthiasmatt, @nibiruheisenberg).
This is useful so that you can run every part of the package code without needing to visit other repositories.

Set up a `.env` file to set environment variables for the tests.
The variables used in the CI build can be found in the `env` section of the [`pytests.yml` workflow](.github/workflows/pytests.yml):

```yaml
jobs:
  tests:
    env: 
      # https://www.notion.so/nibiru/Resources-and-Repo-Configs-b31aa8074a2b419d80b0c946ed5efab0
      CHAIN_ID: ${{ secrets.CHAIN_ID }}
      HOST: ${{ secrets.HOST }}
      VALIDATOR_MNEMONIC: ${{ secrets.VALIDATOR_MNEMONIC }}
      GRPC_PORT: ${{ secrets.GRPC_PORT }}
      LCD_PORT: ${{ secrets.LCD_PORT }}
```

You'll need an `.env` configuration like this.

```sh
# Example configuration for the Nibiry Python SDK
HOST="..."
VALIDATOR_MNEMONIC="..."
GRPC_PORT="..."
LCD_PORT="..."
CHAIN_ID="..."
```

#### Running the tests with `poetry` + `pytest`

After following the instructions for setting up `poetry`, you can run the tests with `poetry run pytest`:

```sh
poetry run pytest -p no:warnings # silences warnings
```

#### (option B). Install the `nibiru-py` package with `pip`

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

## Makefile and Protocol Buffers

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
