Getting Started
===============

Installation
------------

Requires Python 3.7+
``nibiru-py`` is available on `PYPI <https://pypi.python.org/pypi/nibiru-py/>`_.
Install with ``pip``:

.. code:: bash

    pip install nibiru-py


Quick start
-----------

To interact with the chain, you will need to create an account. 
You can create a new account using the CLI command 

.. code:: python

    import nibiru
    from nibiru.common import Side

    # Use the mnemonic from your account
    MNEMONIC = ""guard cream ..."

    # Create a SDK object with your mnemonic
    trader = nibiru.Sdk.authorize(MNEMONIC)

    # Open a long position of axlwbtc for 1000 unusd and 10 leverage
    trader.tx.perp.open_position(
        sender=trader.address,
        token_pair="axlwbtc:unusd",
        side=Side.BUY,
        quote_asset_amount=1000,
        leverage=10,
        base_asset_amount_limit=0,
    )

    # You can query the position with the queries of the perp module
    print(trader.query.perp.trader_position(token_pair="axlwbtc:unusd", trader=trader.address))


Using a different chain
-----------------------

You can connect to any chain (localnet, testnet or mainnet) using this python SDK. By default, it will try to look for 
a chain on your localnet, but you can connect to a remote node by running the following commands

.. code:: python

    import nibiru

    # Configure the network we want to connect to (in this case private testnet).
    network = nibiru.Network(
        lcd_endpoint='https://lcd.nibiru.fi:1317',
        grpc_endpoint=f'https://rpc.nibiru.fi:9090',
        grpc_exchange_endpoint=f'https://rpc.nibiru.fi:9090',
        chain_id="nibiru-testnet-3",
        fee_denom='unibi',
        env='local',
    )

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
    trader.tx.perp.open_position(
        sender=trader.address,
        token_pair="axlwbtc:unusd",
        side=Side.BUY,
        quote_asset_amount=1000,
        leverage=10,
        base_asset_amount_limit=0,
    )    


