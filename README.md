# Python SDK - Nibiru Chain    <!-- omit in toc -->

> Python-based client for interacting with the Nibiru blockchain.

<!-- Badges -->

[![Nibiru Test workflow][tests-badge]][tests-workflow]
[![Examples tests][examples-badge]][tests-example]
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
[discord-badge]: https://dcbadge.vercel.app/api/server/nibirufi?style=flat
[discord-url]: https://discord.gg/nibirufi
[license-badge]: https://img.shields.io/badge/License-MIT-blue.svg
[license-link]: https://github.com/NibiruChain/py-sdk/blob/master/LICENSE
[tests-badge]: https://github.com/NibiruChain/py-sdk/actions/workflows/pytests.yml/badge.svg
[examples-badge]: https://github.com/NibiruChain/py-sdk/actions/workflows/notebooks.yml/badge.svg
[tests-workflow]: https://github.com/NibiruChain/py-sdk/actions/workflows/pytests.yml
[tests-example]: https://github.com/NibiruChain/py-sdk/actions/workflows/notebooks.yml

The `nibiru` package allows you to index, query, and send transactions on Nibiru Chain using Python. It provides access to market data for analysis, visualization, indicator development, algorithmic trading, strategy backtesting, bot programming, and related software engineering.

The package is intended to be used by coders, developers, technically-skilled traders and  data-scientists for building trading algorithms.

## Try running nibiru sdk online

Open the google collab link below to try running Niburu code online: 

<a href="https://colab.research.google.com/github/NibiruChain/py-sdk/blob/main/examples/colab_notebook.ipynb" target="_blank">
<p align="center">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" style="width: 300px;">
</p>
</a>

Or go to the [examples folder](examples) to see the codes and run Jupyter notebooks locally.

## Installation
```bash
pip install nibiru  # requires Python 3.8+
```

## Usage

### Querying the chain

```python
import json
from nibiru import Network, ChainClient

client = ChainClient(Network.testnet(2))

# Query perp markets
print(json.dumps(client.query.perp.markets(), indent=4))

# Query trader's positions
print(
  json.dumps(
    client.query.perp.all_positions(
      trader="nibi1jle8khj3aennq24zx6g93aam9rt0fqhgyp4h52"
    ),
    indent=4)
)
```

### Submitting transactions to the chain

To send a tx you need to authenticate using your wallet mnemonic or private key.

To create a new wallet, generate a mnemonic key using any service or using SDK call.

```python
import json
import nibiru
from nibiru import Network, ChainClient, Msg, PrivateKey

mnemonic, private_key = PrivateKey.generate()
print(mnemonic)
# Example OUTPUT:
# enlist satisfy inspire hobby romance caught great neither kitchen unfair cage awesome update fade object eagle sun ordinary again journey spell gown tiger spin

# Your wallet address
print(private_key.to_public_key().to_address().to_acc_bech32())
# Example OUTPUT:
# nibi1efsh4dq3ve58dgu68rxp8cfe4mgf89el0qfucm
```

Store your mnemonic key in a safe place and use it going forward. 

Use faucet to get some test tokens into your wallet: https://app.nibiru.fi/faucet

Сreate your chain client and authenticate with the mnemoniс generated

```python
mnemonic = "put your mnemonic here..."
client = ChainClient(network=Network.testnet(2))
client.authenticate(mnemonic=mnemonic)
print(client.address)
```

Check your bank balances. If the faucet succeded - your wallet should not be empty.

```python
print(client.query.get_bank_balances(client.address))
```

### Send tx

```python
output = client.tx.execute_msgs(
  Msg.perp.open_position(
    pair=pair,
    is_long=True,
    margin=10,
    leverage=2,
  )
)
print(output)
```

You can broadcast any available transaction by passing its corresponding `Msg` to the `client.tx.execute_msgs` function.

## Documentation Website

Documentation can be found here: [Nibiru-py documentation](https://nibiru-py.readthedocs.io/en/latest/index.html)

- Learn more about opening and managing your spot and perp positions [here](https://nibiru-py.readthedocs.io/en/latest/nibiru.sdks.tx.html#nibiru-sdks-tx-package)
- Learn about querying the chain using the Sdk [here](https://nibiru-py.readthedocs.io/en/latest/nibiru.clients.html#nibiru-clients-package)

## Contributing

Please read [HACKING.MD](HACKING.md) for developer environment setup.
