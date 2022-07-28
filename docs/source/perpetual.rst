Perp Positions
==============

A perpetual contract, or perp, is a type of crypto-native derivative
that enables traders to speculate on price movements without holding the
underlying asset. Nibiru allows traders to trade perps with leverage.

-  `Mark Price and Index Price`_
-  `Leverage and Perp Position Value`_
-  `Margin and Margin Ratio`_

Mark Price and Index Price
--------------------------

Mark Price
^^^^^^^^^^

The **mark price** is the value of the derivative asset (the perp) on
the exchange. Mark price is used to calculate **profits and losses
(PnL)** and determines whether a position has enough collateral backing
it to stay “above water” or if it should be liquidated. The term “mark
price” gets its name from the fact that it describes a position’s
**mark-to-market PnL**, the profit or loss to be realized over the
contract period based on current market conditions (perps exchange
price).

The mark price can be accessed for any market using the vpool submodule queries.

.. code:: python

    from nibiru import Sdk, TxConfig
    from nibiru.common import TxType

    MNEMONIC = "guard cream ..."

    tx_config = TxConfig(tx_type=TxType.BLOCK)

    trader = Sdk.authorize(MNEMONIC).with_config(tx_config)
    trader.query.vpool.all_pools()

    '''
    Output:

    {
        "pools": [
            {
                "base_asset_reserve": 500.0,
                "fluctuation_limit_ratio": 1.0,
                "max_oracle_spread_ratio": 1.0,
                "pair": {
                    "token0": "ubtc",
                    "token1": "unusd"
                },
                "quote_asset_reserve": 10000000.0,
                "trade_limit_ratio": 1.0
            }
        ]
    }
    '''

Index Price
^^^^^^^^^^^

The value of a perp’s underlying asset is referred to as the **index
price**. For example, a BTC:USD perp has BTC as its **base asset** and
dollar collateral such as USDC as could be its **quote asset**. The
dollar value of BTC on spot exchanges is the index price of the BTC:USD
perp. Thus we’d call BTC **“the underlying”**. Usually, the index price
is taken as the average of spot prices across major exchanges.

.. code:: python

    trader.query.pricefeed.price("axlwbtc:unusd")

    '''
    Output:
    {
        "price": {
            "pair_id": "axlwbtc:unusd",
            "price": 20776.0
        }
    }
    '''

Some trading strategies can be built on the difference between mark price
and index price.

Leverage and Perp Position Value
--------------------------------

Position Size
^^^^^^^^^^^^^

Suppose a trader wanted exposure to 5 ETH through the purchase of a
perpetual contract. On Nibi-Perps, going long on 5 ETH means that the
trader buys the ETH perp with a **position size** of 5. Position size is
computed as the position notional mutlipled by the mark price of the
asset.

.. code:: python

   k = baseReserves * quoteReserves
   notionalDelta = margin * leverage # (leverage is negative if short)
   baseReservesAfterSwap = k / (quoteReserves + notionalDelta)
   position_size = baseReserves - baseReservesAfterSwap

Position Notional Value
^^^^^^^^^^^^^^^^^^^^^^^

The notional value of the position, or **position notional**, is the
total value a position controls in units of the quote asset. Notional
value expresses the value a derivatives contract theoretically controls.
On Nibiru, it is defined more concretely by

.. code:: python

   positionNotional = abs(quoteReserves - k / (baseReserves + position_size))
   leverage = positionNotional / margin

Let’s say that the mark price of ether is $3000 in our previous example.
This implies that the trader with a long position of size 5 has a
position notional of $15,000. And if the trader has 10x **leverage**,
for example, she must have put down $1500 as margin (collateral backing
the position).

Open a position
^^^^^^^^^^^^^^^

The python package helps to create and open short and long positions.

.. code:: python

    trader.tx.perp.open_position(
        trader.address,                 # The address of the trader
        token_pair="axlwbtc:unusd",     # The market to interact with
        side=Side.BUY,                  # Either Side.BUY or Side.SELL
        quote_asset_amount=23000,       # Margin for the position
        leverage=5,                     # Leverage of the position
        base_asset_amount_limit=4.5,    # Minimum amount of base received for the transaction
    )

Margin and Margin Ratio
-----------------------

**Margin** is the amount of collateral used to back a position. Margin
is expressed in units of the quote asset. At genesis, Nibi-Perps uses
USDC as the primary quote asset.

The margin ratio is defined by:

::

   marginRatio = (margin + unrealizedPnL) / positionNotional

Here, ``unrealizedPnL`` is computed using either the mark price or the
15 minute TWAP of mark price; the higher of the two values is used when
evaluating liquidation conditions.

When the virtual price is not within the spread tolerance to the index
price, the margin ratio used is the highest value between a calculation
with the index price (oracle based on underlying) and the mark price
(derivative price).

Another good way to think about margin ratio is as the inverse of a
position’s effective leverage. I.e. if a trader puts down $100 as margin
with 5x leverage, the notional is $500 and the margin ratio is 20%,
which is equivalent ot ``1 / leverage``.

Once the position is open, I can monitor the health of my position
along with the unrealized pnl by calling the function trader position
from the query call of the perp module.

.. code:: python

    trader.query.perp.trader_position(
        token_pair="axlwbtc:unusd", 
        trader=trader.address
    )

    '''
    Output:
    {
        "margin_ratio": 0.2,
        "position": {
            "block_number": 5,
            "last_update_cumulative_premium_fraction": 0.0,
            "margin": 23000000000.0,
            "open_notional": 115000000000.0,
            "pair": {
                "token0": "axlwbtc",
                "token1": "unusd"
            },
            "size": 5684626.791893228,
            "trader_address": "nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl"
        },
        "position_notional": 115000000000.0,
        "unrealized_pnl": 1.27e-15
    }
    '''


.. _Perp Positions: #perp-positions
.. _Mark Price and Index Price: #mark-price-and-index-price
.. _Leverage and Perp Position Value: #leverage-and-perp-position-value
.. _Margin and Margin Ratio: #margin-and-margin-ratio
.. _Funding Payments: #funding-payments
.. _Virtual Pools: #virtual-pools
.. _Liquidations: #liquidations
.. _References: #references

References
----------

-  Index Price and Mark Price. BTSE. `[support.btse.com]`_
-  Notional Value vs. Market Value: An Overview. Investopedia.
   `[investopedia.com]`_
-  Differences Between Isolated Margin and Cross Margin - Binance.
   `[binance.com]`_
-  Isolated and Cross Margin - BitMex. `[bitmex.com]`_
-  Funding. FTX Crypto Derivatives Exchange. `[help.ftx.com]`_

.. _[support.btse.com]: https://support.btse.com/en/support/solutions/articles/43000557589-index-price-and-mark-price
.. _[investopedia.com]: https://www.investopedia.com/ask/answers/050615/what-difference-between-notional-value-and-market-value.asp
.. _[binance.com]: https://www.binance.com/en/support/faq/b4e9e6ad70934bd082e8e09e33e69513
.. _[bitmex.com]: https://www.bitmex.com/app/isolatedMargin
.. _[help.ftx.com]: https://help.ftx.com/hc/en-us/articles/360027946571-Funding