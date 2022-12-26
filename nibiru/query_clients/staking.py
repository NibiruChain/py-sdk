from grpc import Channel
from nibiru_proto.proto.cosmos.staking.v1beta1 import query_pb2 as staking_type
from nibiru_proto.proto.cosmos.staking.v1beta1 import query_pb2_grpc as staking_query

from nibiru.query_clients.util import QueryClient, deserialize, get_page_request


class StakingQueryClient(QueryClient):
    """
    StakingQueryClient allows to query the endpoints made available
    by the Nibiru Chain's staking module.
    """

    def __init__(self, channel: Channel):
        self.api = staking_query.QueryStub(channel)

    def pool(self) -> dict:
        """
        Query the current staking pool values

        Example Return Value::

        ```json
        {
          "not_bonded_tokens": "49100355602",
          "bonded_tokens": "2419845520076726"
        }
        ```

        Returns:
            dict: the staking pool values by bounded and not bounded

        """
        return self.query(
            api_callable=self.api.Pool,
            req=staking_type.QueryPoolRequest(),
        )

    def delegation(self, delegator_addr: str, validator_addr: str) -> dict:
        """
        Query a delegation based on address and validator address

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
        """
        return self.query(
            api_callable=self.api.Delegation,
            req=staking_type.QueryDelegationRequest(
                delegator_addr=delegator_addr, validator_addr=validator_addr
            ),
        )

    def delegations(self, delegator_addr: str, **kwargs) -> dict:
        """
        Query all delegations made by one delegator

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
        """
        return self.query(
            api_callable=self.api.DelegatorDelegations,
            req=staking_type.QueryDelegatorDelegationsRequest(
                delegator_addr=delegator_addr,
                pagination=get_page_request(kwargs),
            ),
        )

    def delegations_to(self, validator_addr: str, **kwargs) -> dict:
        """
        Query all delegations made to one validator

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
        """
        return self.query(
            api_callable=self.api.ValidatorDelegations,
            req=staking_type.QueryValidatorDelegationsRequest(
                validator_addr=validator_addr,
                pagination=get_page_request(kwargs),
            ),
        )

    def historical_info(self, height: int) -> dict:
        """
        Query historical info at given height

        Args:
            height: at which we want to get historical info

        Returns:
            dict: the historical information
        """
        return self.query(
            api_callable=self.api.HistoricalInfo,
            req=staking_type.QueryHistoricalInfoRequest(height=height),
        )

    def params(self) -> dict:
        """
        Query the current staking parameters information

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
        """
        return self.query(
            api_callable=self.api.Params,
            req=staking_type.QueryParamsRequest(),
        )

    def redelegations(
        self, delegator_addr: str, dst_validator_addr: str, **kwargs
    ) -> dict:
        """
        Query all redelegations records for one delegator

        Args:
            delegator_addr: the address of the delegator
            dst_validator_addr: a validator address
        """
        return self.query(
            api_callable=self.api.Redelegations,
            req=staking_type.QueryRedelegationsRequest(
                delegator_addr=delegator_addr,
                dst_validator_addr=dst_validator_addr,
                pagination=get_page_request(kwargs),
            ),
        )

    def unbonding_delegation(self, delegator_addr: str, validator_addr: str) -> dict:
        """
        Query an unbonding-delegation record based on delegator and validator address

        Args:
            delegator_addr: the delegator address
            validator_addr: the validator address
        """
        return self.query(
            api_callable=self.api.UnbondingDelegation,
            req=staking_type.QueryUnbondingDelegationRequest(
                validator_addr=validator_addr,
                delegator_addr=delegator_addr,
            ),
        )

    def unbonding_delegations(self, delegator_addr: str, **kwargs) -> dict:
        """
        Query all unbonding-delegations records for one delegator

        Args:
            delegator_addr: the delegator address
        """
        return self.query(
            api_callable=self.api.DelegatorUnbondingDelegations,
            req=staking_type.QueryDelegatorUnbondingDelegationsRequest(
                delegator_addr=delegator_addr,
                pagination=get_page_request(kwargs),
            ),
        )

    def unbonding_delegations_from(self, validator_addr: str, **kwargs) -> dict:
        """
        Query all unbonding delegations from a validator

        Args:
            validator_addr: the validator address
        """
        return self.query(
            api_callable=self.api.ValidatorUnbondingDelegations,
            req=staking_type.QueryValidatorUnbondingDelegationsRequest(
                validator_addr=validator_addr,
                pagination=get_page_request(kwargs),
            ),
        )

    def validator(self, validator_addr: str) -> dict:
        """
        Query a validator

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
        """
        return self.query(
            api_callable=self.api.Validator,
            req=staking_type.QueryValidatorRequest(
                validator_addr=validator_addr,
            ),
        )

    def validators(self, **kwargs) -> dict:
        """
        Query for all validators

        Example Return Value::
            Same as the return value of the 'validator' function except as a list

        Returns:
            dict: the info of all validators

        """
        proto_output = self.query(
            api_callable=self.api.Validators,
            req=staking_type.QueryValidatorsRequest(
                pagination=get_page_request(kwargs),
            ),
            should_deserialize=False,
        )
        return deserialize(proto_output)
