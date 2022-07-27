General Endpoints
=================


`Get the perpetual parameters`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Query the parameters for the perpetual module by running;

.. code:: python

    parameters = trader.query.perp.params()

`Get the list of open markets to trade on`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can query all the virtual pools by running:

.. code:: python

    markets = trader.query.vpool.all_pools()


`Get the price in quote of a denom`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can get the current price fo the base in quote by running:

.. code:: python

    trader.query.vpool.base_asset_price("axlwbtc:unusd", Side.BUY, "10000")


`Get the current position for a trader and a token pair`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can get information about your current position by running:

.. code:: python

    trader.query.perp.trader_position(
        token_pair="axlwbtc:unusd",
        trader=trader.address
    )