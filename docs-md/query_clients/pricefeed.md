Module nibiru.query_clients.pricefeed
=====================================

Classes
-------

`PricefeedQueryClient(channel: grpc.Channel)`
:   Pricefeed allows to query the endpoints made available by the Nibiru Chain's Pricefeed module.

    ### Ancestors (in MRO)

    * nibiru.query_clients.util.QueryClient

    ### Methods

    `markets(self)`
    :

    `oracles(self, pair_id: str)`
    :

    `params(self)`
    :

    `price(self, pair_id: str)`
    :

    `prices(self)`
    :

    `raw_prices(self, pair_id: str)`
    :
