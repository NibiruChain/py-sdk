# Python SDK - Nibiru Chain    <!-- omit in toc -->

> Python-based client for interacting with the Nibiru blockchain.

<!-- Badges -->

[![Nibiru Test workflow][tests-badge]][tests-workflow]
[![Nibiru examples tests][examples-badge]][tests-example]
[![PyPI Version][pypi-image]][pypi-url]
[![][documentation-image]][documentation-url]
[![][discord-badge]][discord-url]
[![][stars-image]][stars-url]
[![MIT license][license-badge]][license-link]

<!-- Badges links -->

<!-- pypi -->
[pypi-image]: https://img.shields.io/pypi/v/nibiru
[pypi-url]: https://pypi.org/project/nibiru/
[stars-image]: https://img.shields.io/github/stars/NibiruChain?style=social
[stars-url]: https://github.com/NibiruChain
[documentation-image]: https://readthedocs.org/projects/nibiru-py/badge/?version=latest
[documentation-url]: https://nibiru-py.readthedocs.io/en/latest/?badge=latest
[discord-badge]: https://dcbadge.vercel.app/api/server/sgPw8ZYfpQ?style=flat
[discord-url]: https://discord.gg/sgPw8ZYfpQ
[license-badge]: https://img.shields.io/badge/License-MIT-blue.svg
[license-link]: https://github.com/NibiruChain/py-sdk/blob/master/LICENSE
[tests-badge]: https://github.com/NibiruChain/py-sdk/actions/workflows/pytests.yml/badge.svg
[examples-badge]: https://github.com/NibiruChain/py-sdk/actions/workflows/notebooks.yml/badge.svg
[tests-workflow]: https://github.com/NibiruChain/py-sdk/actions/workflows/pytests.yml
[tests-example]: https://github.com/NibiruChain/py-sdk/actions/workflows/notebooks.yml

The `nibiru` package allows you to index, query, and send transactions on Nibiru Chain using Python. It provides access to market data for analysis, visualization, indicator development, algorithmic trading, strategy backtesting, bot programming, and related software engineering.

The package is intended to be used by coders, developers, technically-skilled traders and  data-scientists for building trading algorithms.

#### README Contents

- [Python SDK Tutorial](#python-sdk-tutorial)
- [Installation from `PyPI`](#installation-from-pypi)
- [Usage](#usage)
  - [Ex: Creating a wallet and SDK client](#ex-creating-a-wallet-and-sdk-client)
  - [Ex: Using the faucet](#ex-using-the-faucet)
  - [Ex: Querying chain state](#ex-querying-chain-state)
  - [Ex: Submitting transactions](#ex-submitting-transactions)
- [Documentation Website](#documentation-website)
- [Contributing](#contributing)

## Python SDK Tutorial

<a href="https://colab.research.google.com/github/NibiruChain/py-sdk/blob/master/examples/collab_notebook.ipynb" target="_blank">
<p align="center">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" style="width: 300px;">
</p>
</a>

## Installation from `PyPI`

```bash
pip install nibiru  # requires Python 3.7+
```

You may need to update `pip` to get this to run:

```bash
python -m pip install --upgrade pip
```

## Usage

### Ex: Creating a wallet and SDK client

```python
from nibiru import wallet

# Save the mnemonic for later
mnemonic, private_key = wallet.PrivateKey.generate()
```

After, creating an account, you can create an `Sdk` instance.

```python
import nibiru

network = nibiru.network.Network.testnet(2)
sdk = nibiru.Sdk.authorize(mnemonic)
  .with_network(network)
```

The `Sdk` class creates an interface to sign and send transactions or execute
queries. It is associated with:
- A transaction signer (wallet), which is configured from existing mnemonic to recover a `PrivateKey`.
- A `Network`, which specifies the RPC, LCD, and gRPC endpoints for connecting to Nibiru Chain.
- An optional `TxConfig` for changing gas parameters.

### Ex: Using the faucet

```python
import requests

requests.post(
    "https://faucet.testnet-2.nibiru.fi/",
    json={
        "address": sdk.address,
        "coins": ["10000000unibi", "100000000000unusd"],
    },
)
```

### Ex: Querying chain state

```python
# Querying the token balances of the account
sdk.query.get_bank_balances(sdk.address)

# Querying from the vpool module
query_resp = sdk.query.vpool.all_pools()
print(query_resp)
# Queries from other modules can be accessed from "sdk.query.module"
```

### Ex: Submitting transactions

```python
# version 0.16.3
from nibiru import Msg

tx_resp = sdk.tx.execute_msgs(
    Msg.perp.open_position(
        sender=sdk.address,
        pair="ubtc:unusd",
        is_long=True,
        quote_asset_amount=10,
        leverage=10,
        base_asset_amount_limit=0,
    )
)
```

You can broadcast any available transaction by passing its corresponding `Msg` to the `sdk.tx.execute_msgs` function.

## Documentation Website

Documentation can be found here: [Nibiru-py documentation](https://nibiru-py.readthedocs.io/en/latest/index.html)

- Learn more about opening and managing your spot and perp positions [here](https://nibiru-py.readthedocs.io/en/latest/nibiru.sdks.tx.html#nibiru-sdks-tx-package)
- Learn about querying the chain using the Sdk [here](https://nibiru-py.readthedocs.io/en/latest/nibiru.clients.html#nibiru-clients-package)

## Contributing

Please read [HACKING.MD](HACKING.md) for developer environment setup.
