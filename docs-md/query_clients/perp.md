Module pysdk.query_clients.perp
===============================

Classes
-------

`PerpQueryClient(channel: grpc.Channel)`
:   Perp allows to query the endpoints made available by the Nibiru Chain's PERP module.

    ### Ancestors (in MRO)

    * pysdk.query_clients.util.QueryClient

    ### Methods

    `all_positions(self, trader: str) ‑> Dict[str, dict]`
    :   Args:
            trader (str): Address of the owner of the positions

        Returns:
            Dict[str, dict]: All of the open positions for the 'trader'.

        Example Return Value:

        ```json
        {
          "ubtc:unusd": {
            "block_number": 1137714,
            "margin_ratio_index": 0.0,
            "margin_ratio_mark": 0.09999999999655101,
            "position": {
            "block_number": 1137714,
            "latest_cumulative_premium_fraction": 17233.436302191654,
            "margin": 10.0,
            "open_notional": 100.0,
            "pair": "ubtc:unusd",
            "size": -0.00545940925278242,
            "trader_address": "nibi10gm4kys9yyrlqpvj05vqvjwvje87gln8nsm8wa"
            },
            "position_notional": 100.0,
            "unrealized_pnl": -5.079e-15
          }
        }
        ```

    `params(self)`
    :   Get the parameters of the perp module.

        Example Return Value::

        ```json
        {
          "feePoolFeeRatio": 0.001,
          "ecosystemFundFeeRatio": 0.001,
          "liquidationFeeRatio": 0.025,
          "partialLiquidationRatio": 0.25,
          "epochIdentifier": "30 min",
          "twapLookbackWindow": "900s"
        }
        ```

        Returns:
            dict: The current parameters for the perpetual module

    `position(self, pair: str, trader: str) ‑> dict`
    :   Get the trader position. Returns information about position notional, margin ratio
        unrealized pnl, size of the position etc.

        Args:
            pair (str): The token pair
            trader (str): The trader address

        Example Return Value::

        ```json
        {
          "position": {
            "traderAddress": "nibi1zaavvzxez0elund",
            "pair": "ubtc:unusd",
            "size": 11.241446725317692,
            "margin": 45999.99999999999,
            "openNotional": 230000.0,
            "lastUpdateCumulativePremiumFraction": "0",
            "blockNumber": "278"
          },
          "positionNotional": 230000.0,
          "unrealizedPnl": 1.024e-20,
          "marginRatioMark": 0.2,
          "marginRatioIndex": 0.2
        }
        ```

        Returns:
            dict: The output of the query
