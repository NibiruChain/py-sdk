Module nibiru.query_clients.staking
===================================

Classes
-------

`StakingQueryClient(channel: grpc.Channel)`
:   StakingQueryClient allows to query the endpoints made available
    by the Nibiru Chain's staking module.

    ### Ancestors (in MRO)

    * nibiru.query_clients.util.QueryClient

    ### Methods

    `delegation(self, delegator_addr: str, validator_addr: str) ‑> dict`
    :   Query a delegation based on address and validator address

    `delegations(self, delegator_addr: str, **kwargs) ‑> dict`
    :   Query all delegations made by one delegator

    `delegations_to(self, validator_addr: str, **kwargs) ‑> dict`
    :   Query all delegations made to one validator

    `historical_info(self, height: int) ‑> dict`
    :   Query historical info at given height

    `params(self) ‑> dict`
    :   Query the current staking parameters information

    `pool(self) ‑> dict`
    :   Query the current staking pool values

    `redelegations(self, delegator_addr: str, dst_validator_addr: str, **kwargs) ‑> dict`
    :   Query all redelegations records for one delegator

    `unbonding_delegation(self, delegator_addr: str, validator_addr: str) ‑> dict`
    :   Query an unbonding-delegation record based on delegator and validator address

    `unbonding_delegations(self, delegator_addr: str, **kwargs) ‑> dict`
    :   Query all unbonding-delegations records for one delegator

    `unbonding_delegations_from(self, validator_addr: str, **kwargs) ‑> dict`
    :   Query all unbonding delegations from a validator

    `validator(self, validator_addr: str) ‑> dict`
    :   Query a validator

    `validators(self, **kwargs) ‑> dict`
    :   Query for all validators
