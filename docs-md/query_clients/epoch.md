Module nibiru.query_clients.epoch
=================================

Classes
-------

`EpochQueryClient(channel: grpc.Channel)`
:   EpochQueryClient allows to query the endpoints made available by the Nibiru Chain's epoch module.
    This module is used to time out certain events like for example funding rate payments.

    ### Ancestors (in MRO)

    * nibiru.query_clients.util.QueryClient

    ### Methods

    `current_epoch(self, epoch_identifier: str) ‑> dict`
    :

    `epoch_infos(self) ‑> dict`
    :
