# HACKING - py-sdk

Guidelines for developing and contributing to the Nibiru Python SDK.

- [HACKING - py-sdk](#hacking---py-sdk)
  - [Environment Setup](#environment-setup)
    - [Pyenv for managing multiple Python interpreters](#pyenv-for-managing-multiple-python-interpreters)
  - [Installing `poetry` for dependency resolution and publishing packages](#installing-poetry-for-dependency-resolution-and-publishing-packages)
    - [Installing external dependencies](#installing-external-dependencies)
  - [Running tests](#running-tests)
      - [Setting environment variables](#setting-environment-variables)
      - [Environment Variables - Local](#environment-variables---local)
      - [Environment variables in GitHub Actions](#environment-variables-in-github-actions)
      - [Running the tests with `poetry` + `pytest`](#running-the-tests-with-poetry--pytest)
      - [(option B). Install the `nibiru` package with `pip`](#option-b-install-the-nibiru-package-with-pip)
  - [Docgen](#docgen)
  - [Publishing on PyPI](#publishing-on-pypi)
    - [poetry version subcommands](#poetry-version-subcommands)
  - [Makefile and Protocol Buffers](#makefile-and-protocol-buffers)
  - [Linting](#linting)


## Environment Setup

Our recommended setup for a professional dev environment is to use `pyenv` in combination with `poetry`.

- `pyenv` is a tool for installing and managing Python interpreters. This will let you seamlessly switch between Python versions.
- `poetry` is used for managing virtual environments, dependency resolution, package installations, package building, and package publishing.
- We assume you're on a Unix machine such as WSL2 Ubuntu, MacOS, or a common Linux distro.

Currently, `nibiru` is created with Python 3.7.16. It may be compatible with higher versions, but we only run end-to-end tests in 3.7.16.

### Pyenv for managing multiple Python interpreters

If you're on MacOS or a common Linux distro, you can install `pyenv` with brew.

```bash
brew install pyenv
```

You'll then need to add the following snippet to your shell config, e.g. your `.bash_profile`, `.bashrc`, or `.zshrc`.

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

After using `source` on your config or restarting the shell, you should have the `pyenv` root command.

The command use to install any version of python is `pyenv install`. Display additional info for this command with `pyenv install --help`.

```bash
pyenv install 3.7.16 # example for nibiru
```

Once you have a version installed, you can print out the versions on your machine with:

```bash
pyenv versions
```

```
# example output
  system
* 3.7.16 (set by /home/realu/.python-version)
  3.10.4
```

In this example, I have 2 different interpreters installed on my machine. The one with the `*` is currently set as my **global interpreter**. This is set manually using the `pyenv global` command.

```bash
pyenv global 3.10.4   # switches the global interpreter to 3.10.4
```

You can verify this works as expected using `python --version`. You may be familiar with using `python3` as the command instead of `python`. With `pyenv`, this is not necessary.

Additional usage and installation instructions can be found in the [pyenv repo](https://github.com/pyenv/pyenv).

## Installing `poetry` for dependency resolution and publishing packages

Reference: [Poetry docs](https://python-poetry.org/docs/)

Poetry can be installed with both `curl` and `pip`. We recommended using `curl` so that it will be global to your machine.

NOTE We highly, highly, highly recommend that you DO NOT use `brew` to install `poetry`.
If you use `brew`, it's going to install directly to your system, which prevents you from being able to leverage `pyenv` to seamlessly switch between Python interpreters.

```bash
# installation with pip: recommended option in tandem with pyenv
pip install poetry
```

```bash
# For UNIX systems - installation with curl
curl -sSL https://install.python-poetry.org | python3 -
```

After this installation command, add the `poetry` binary to the path in your shell config (if it's not done automatically).

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Installing external dependencies

The `nibiru` project is defined by its `pyproject.toml`. At the root of the repo, simply call:

```bash
poetry install
```

This will resolve dependencies between each of the project's packages and install them into a virtual environment.

## Generating nibiru protos

```bash
poetry run ./scripts/proto-gen-py.sh
```

## Running tests

#### Setting environment variables

There's currently a "devnet" running in GCP that the CI workflows use. You can find these secrets at [this notion page](https://www.notion.so/nibiru/Resources-and-Repo-Configs-b31aa8074a2b419d80b0c946ed5efab0) if you have access to it or contact one of the `CODEOWNERS` (@Unique-Divine, @matthiasmatt, @nibiruheisenberg).
This is useful so that you can run every part of the package code without needing to visit other repositories.

You'll need to set up a `.env` configuration file to set environment variables for the tests.

#### Environment Variables - Local


```bash
# Example configuration for the Nibiry Python SDK
HOST="..."
VALIDATOR_MNEMONIC="..."
TENDERMINT_RPC_ENDPOINT="http://...:26657"
LCD_ENDPOINT="http://...:1317"
GRPC_ENDPOINT="...:9090"
WEBSOCKET_ENDPOINT="ws://...:26657/websocket"
CHAIN_ID="..."
```

#### Environment variables in GitHub Actions

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

#### Running the tests with `poetry` + `pytest`

After following the instructions for setting up `poetry`, you can run the tests with `poetry run pytest`:

```bash
poetry run pytest -p no:warnings # silences warnings

poetry run pytest --slow -p no:warnings # to include slowly running tests
```

#### (option B). Install the `nibiru` package with `pip`

  ```bash
  # from local
  # build and install
  pip install .

  # from local build
  pip uninstall nibiru
  pip install nibiru --no-index --find-links /path/to/nibiru/py-sdk/dist

  # from pypi
  pip uninstall nibiru
  pip install nibiru
  ```

## Docgen

```bash
poetry run pdoc nibiru -o=docs-md-pdoc -f --skip-errors
```

See https://pdoc3.github.io/pdoc/


## Publishing on PyPI

1. Changing the version number in the `pyproject.toml` changes the package version number. You can either edit it manually or use one of the `poetry version [bump-rule]` commands.
2. After changing the package version, use `poetry build` to add a distribution for this version to the `dist` directory.
3. Set your PyPI username and password as the environment variables `PYPI_USERNAME` and `PYPI_PASSWORD`.
4. Publish in the following manner.
    ```bash
    poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
    ```

### poetry version subcommands

For the `poetry version` command, using any bump rule with a valid semver string will change the version inside `pyproject.toml`. For example,

```bash
poetry version patch # moves from x.y.14 to x.y.15
poetry version minor # moves from x.5.z to x.6.0
poetry version major # moves from 3.y.z to 4.0.0
```

The list of bump rules includes:
patch, minor, major, prepatch, preminor, premajor, prerelease.

You specify updates to publish using the commit (or PR) title with `bump-[version-keyword]`.

So the list of available keywords you an put in a PR includes
- `bump-patch`:
- `bump-patch`: 0.0.0 → 0.0.1
- `bump-minor`: 0.0.* → 0.1.0
- `bump-major`: 0.*.* → 1.0.0
- `bump-prepatch`: 0.0.0 → 0.0.1-alpha0
- `bump-prerelease`: equivalent to `bump-prepatch`
- `bump-preminor`: 0.0.* → 0.1.0-alpha0
- `bump-premajor`: 0.*.* → 1.0.0-alpha0

These guidelines are in the release.yml for future reference.

## Makefile and Protocol Buffers

Protobuf-generated types from NibiruChain/nibiru are published under `nibiru_proto` package, which is created in the [NibiruChain/sdk-proto-gen repository](https://github.com/NibiruChain/sdk-proto-gen). Visit this repo for more information.

The entrypoint command is:

```bash
make proto-gen
```

If you get a permissions error such as

```
rm: cannot remove 'proto/proto/epochs/query.proto': Permission denied
```

call `sudo chown -R [USER-NAME] proto` using the name of user directory.
You can find the value for `[USER-NAME]` quickly by running `whoami`. In other words, this should work:

```bash
sudo chown -R $(whoami) proto
```

You're done generating types once you've successfully called

```bash
make proto-gen
poetry build
```

## Linting

Enable git hook which will perform linting before each commit:

```bash
poetry run pre-commit install
```

This will help keep your code clean.
