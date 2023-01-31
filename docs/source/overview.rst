Getting Started
===============

Installation
------------

Requires Python 3.9+
``nibiru`` is available on `PYPI <https://pypi.python.org/pypi/nibiru/>`_.
Install with ``pip``:

.. code:: bash

    pip install nibiru


Quick start
-----------

To interact with the chain, you will need to create an account.
You can create a new account using the CLI command.

.. code:: python

    import nibiru
    import nibiru.msg

    # Use the mnemonic from your account
    MNEMONIC = "guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host"

    # Create a SDK object with your mnemonic
    trader = nibiru.Sdk.authorize(MNEMONIC).with_network(nibiru.Network.devnet(2))

    # Open a long position of ubtc:unusd for 10 unusd and 5 leverage
    trader.tx.execute_msgs(
        nibiru.msg.MsgOpenPosition(
            sender=trader.address,
            pair="ubtc:unusd",
            side=nibiru.Side.BUY,
            quote_asset_amount=10,
            leverage=5,
            base_asset_amount_limit=0,
        )
    )

    # You can query the position with the queries of the perp module
    print(trader.query.perp.position(pair="ubtc:unusd", trader=trader.address))


Using a different chain
-----------------------

You can connect to any chain (localnet, testnet or mainnet) using this python SDK. By default, it will try to look for
a chain on your localnet, but you can connect to a remote node by running the following commands

.. code:: python

    import nibiru

    # Configure the network we want to connect to (in this case private testnet).
    network = nibiru.Network.testnet()

    # Create the sdk object with a specific network
    trader = Sdk.authorize(MNEMONIC).with_network(network)


Async API Calls
---------------

By default, the transactions are sent asynchronously, meaning we post the transaction without waiting for a confirmation
that it was picked by a block. This behavior can be changed using the TxConfig object

.. code:: python

    import nibiru
    from nibiru.common import Side, TxType

    # class TxType(Enum):
    #    SYNC = 1
    #    ASYNC = 2
    #    BLOCK = 3

    tx_config = nibiru.TxConfig(tx_type=TxType.BLOCK)

    # Create the sdk object with a specific tx configuration
    trader = Sdk.authorize(MNEMONIC).with_config(tx_config)

    # This next function will run until the transaction is picked up in a block.
    trader.tx.execute_msgs(
        nibiru.msg.MsgOpenPosition(
            sender=trader.address,
            pair="ubtc:unusd",
            side=nibiru.Side.BUY,
            quote_asset_amount=10,
            leverage=5,
            base_asset_amount_limit=0,
        )
    )
