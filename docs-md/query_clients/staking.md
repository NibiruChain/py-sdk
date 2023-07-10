Module pysdk.query_clients.staking
==================================

Classes
-------

`StakingQueryClient(channel: grpc.Channel)`
:   StakingQueryClient allows to query the endpoints made available
    by the Nibiru Chain's staking module.

    ### Ancestors (in MRO)

    * pysdk.query_clients.util.QueryClient

    ### Methods

    `delegation(self, delegator_addr: str, validator_addr: str) ‑> dict`
    :   Query a delegation based on address and validator address

        Args:
            delegator_addr: the delegator address
            validator_addr: the validator that the delegator has delegated

        Returns:
            dict: the delegation details

        Example Return Value::

        ```json
        {
          "delegation": {
            "delegator_address": "nibi1zpsd7pxvqfcaxevgc2a07q3tgcwgaua92uyg4x",
            "validator_address": "nibivaloper1zpsd7pxvqfcaxevgc2a07q3tgcwgaua9r82npm",
            "shares": "127051284777.000000000000000000"
          },
          "balance": {
            "denom": "unibi",
            "amount": "127051284777"
          }
        }
        ```

    `delegations(self, delegator_addr: str, **kwargs) ‑> dict`
    :   Query all delegations made by one delegator

        Example Return Value::

        ```json
        {
            "delegation_responses": [
                {
                    "delegation": {
                    "delegator_address": "nibi1zpsd7pxvqfcaxevgc2a07q3tgcwgaua92uyg4x",
                    "validator_address": "nibivaloper1zpsd7pxvqfcaxevgc2a07q3tgcwgaua9r82npm",
                    "shares": "127114301897.000000000000000000"
                },
                "balance": {
                    "denom": "unibi",
                    "amount": "127114301897"
                }
            }
        }
        ```

        Args:
            delegator_addr: the address of the delegator

        Returns:
            dict: the delegations that de delegator has

    `delegations_to(self, validator_addr: str, **kwargs) ‑> dict`
    :   Query all delegations made to one validator

        Return Example::

        ```json
        {
        "delegation_responses": [
          {
            "delegation": {
            "delegator_address": "nibi1zpsd7pxvqfcaxevgc2a07q3tgcwgaua92uyg4x",
            "validator_address": "nibivaloper1zpsd7pxvqfcaxevgc2a07q3tgcwgaua9r82npm",
            "shares": "127429922469.000000000000000000"
          },
          "balance": {
            "denom": "unibi",
            "amount": "127429922469"
          }
        ],
        }
        ```

        Args:
            validator_addr: the validator that we want to know the delegations it has

        Returns:
            dict: the list of delegations

    `historical_info(self, height: int) ‑> dict`
    :   Query historical info at given height

        Args:
            height: at which we want to get historical info

        Returns:
            dict: the historical information

    `params(self) ‑> dict`
    :   Query the current staking parameters information

        Example Return Value::

        ```json
        {
          "unbonding_time": "7200s",
          "max_validators": 100,
          "max_entries": 7,
          "historical_entries": 10000,
          "bond_denom": "unibi"
        }
        ```

        Returns:
            dict: the params of the module

    `pool(self) ‑> dict`
    :   Query the current staking pool values

        Example Return Value::

        ```json
        {
          "not_bonded_tokens": "49100355602",
          "bonded_tokens": "2419845520076726"
        }
        ```

        Returns:
            dict: the staking pool values by bounded and not bounded

    `redelegations(self, delegator_addr: str, dst_validator_addr: str, **kwargs) ‑> dict`
    :   Query all redelegations records for one delegator

        Args:
            delegator_addr: the address of the delegator
            dst_validator_addr: a validator address

    `unbonding_delegation(self, delegator_addr: str, validator_addr: str) ‑> dict`
    :   Query an unbonding-delegation record based on delegator and validator address

        Args:
            delegator_addr: the delegator address
            validator_addr: the validator address

    `unbonding_delegations(self, delegator_addr: str, **kwargs) ‑> dict`
    :   Query all unbonding-delegations records for one delegator

        Args:
            delegator_addr: the delegator address

    `unbonding_delegations_from(self, validator_addr: str, **kwargs) ‑> dict`
    :   Query all unbonding delegations from a validator

        Args:
            validator_addr: the validator address

    `validator(self, validator_addr: str) ‑> dict`
    :   Query a validator

        Example Return Value::

        ```json
        {
          "operator_address": "nibivaloper1zpsd7pxvqfcaxevgc2a07q3tgcwgaua9r82npm",
          "consensus_pubkey": {
            "@type": "/cosmos.crypto.ed25519.PubKey",
            "key": "9hFIS+BTJxyWH/OgjH4om2nOWf2p7whS/jmMuEA4gnk="
          },
          "jailed": false,
          "status": "BOND_STATUS_BONDED",
          "tokens": "127702800941",
          "delegator_shares": "127702800941.000000000000000000",
          "description": {
            "moniker": "some val",
            "identity": "info",
            "website": "someweb",
            "security_contact": "",
            "details": "abc"
          },
          "unbonding_height": "0",
          "unbonding_time": "1970-01-01T00:00:00Z",
          "commission": {
            "commission_rates": {
              "rate": "0.100000000000000000",
              "max_rate": "0.300000000000000000",
              "max_change_rate": "0.030000000000000000"
            },
            "update_time": "2022-12-21T17:17:38.806603554Z"
          },
          "min_self_delegation": "1"
        }
        ```

        Args:
            validator_addr: the validator address

        Returns:
            dict: the information from the validator

    `validators(self, **kwargs) ‑> dict`
    :   Query for all validators

        Example Return Value::
            Same as the return value of the 'validator' function except as a list

        Returns:
            dict: the info of all validators
