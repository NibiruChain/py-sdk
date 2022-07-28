# Nibiru Python SDK

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



### Dependencies

**Ubuntu**
```bash
sudo apt install python3.X-dev autoconf automake build-essential libffi-dev libtool pkg-config
```
**Fedora**
```bash
sudo dnf install python3-devel autoconf automake gcc gcc-c++ libffi-devel libtool make pkgconfig
```

**macOS**

```bash
brew install autoconf automake libtool
```

### Quick Start
Installation
```bash
pip install nibiru-py
```

### Usage
Requires Python 3.9+

[Examples](https://github.com/NibiruChain/sdk-python/tree/master/examples)
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

### Development
1. Enable dev env
  ```
  pipenv shell
  pipenv install --dev
  ```

2. Generate proto binding & build
  ```
  make proto-gen
  python -m build     # Run `pip install build` in case this fails
  ```


3. Install pkg
  ```
  # from local
  # build and install
  pip install .

  # from local build
  pip uninstall nibiru-py
  pip install nibiru-py --no-index --find-links /path/to/nibiru/sdk-python/dist

  # from pypi
  pip uninstall nibiru-py
  pip install nibiru-py
  ```
### Linting
Enable git hook which will perform linting before each commit:
```shell
pre-commit install
```
This will keep your code clean.
