Module nibiru.query_clients.vpool
=================================

Functions
---------


`cast_str_to_float_safely(number_str: str) ‑> float`
:

Classes
-------

`VpoolQueryClient(channel: grpc.Channel)`
:   VPool allows to query the endpoints made available by the Nibiru Chain's VPOOL module.

    ### Ancestors (in MRO)

    * nibiru.query_clients.util.QueryClient

    ### Methods

    `all_pools(self)`
    :

    `base_asset_price(self, pair: str, direction: nibiru.pytypes.common.Direction, base_asset_amount: str)`
    :

    `reserve_assets(self, pair: str)`
    :
