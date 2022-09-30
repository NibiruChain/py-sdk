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
        """
        return self.query(
            api_callable=self.api.Pool,
            req=staking_type.QueryPoolRequest(),
        )

    def delegation(self, delegator_addr: str, validator_addr: str) -> dict:
        """
        Query a delegation based on address and validator address
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
        """
        return self.query(
            api_callable=self.api.HistoricalInfo,
            req=staking_type.QueryHistoricalInfoRequest(height=height),
        )

    def params(self) -> dict:
        """
        Query the current staking parameters information
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
        """
        proto_output = self.query(
            api_callable=self.api.Validators,
            req=staking_type.QueryValidatorsRequest(
                pagination=get_page_request(kwargs),
            ),
            should_deserialize=False,
        )
        return deserialize(proto_output)
