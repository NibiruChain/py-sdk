Module nibiru.query_clients.perp
================================

Classes
-------

`PerpQueryClient(channel: grpc.Channel)`
:   Perp allows to query the endpoints made available by the Nibiru Chain's PERP module.

    ### Ancestors (in MRO)

    * nibiru.query_clients.util.QueryClient

    ### Methods

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
