import pytest

from nibiru import Sdk
from nibiru.exceptions import QueryError
from tests import dict_keys_must_match


def get_validator_operator_address(val_node: Sdk):
    """
    Return the first validator and deletator
    """
    validator = val_node.query.staking.validators()["validators"][0]
    return validator["operator_address"]


def test_query_vpool(val_node: Sdk):
    query_resp = val_node.query.staking.pool()
    assert query_resp["pool"]["bonded_tokens"] >= 0
    assert query_resp["pool"]["not_bonded_tokens"] >= 0


def test_query_delegation(val_node: Sdk):
    query_resp = val_node.query.staking.delegation(
        val_node.address,
        get_validator_operator_address(val_node)
    )
    dict_keys_must_match(
        query_resp["delegation_response"],
        [
            "delegation",
            "balance",
        ]
    )


def test_query_delegations(val_node: Sdk):
    query_resp = val_node.query.staking.delegations(val_node.address)
    dict_keys_must_match(
        query_resp["delegation_responses"][0],
        [
            "delegation",
            "balance",
        ]
    )


def test_query_delegations_to(val_node: Sdk):
    query_resp = val_node.query.staking.delegations_to(
        get_validator_operator_address(val_node)
    )
    dict_keys_must_match(
        query_resp["delegation_responses"][0],
        [
            "delegation",
            "balance",
        ]
    )


def test_historical_info(val_node: Sdk):
    with pytest.raises(QueryError, match="not found"):
        val_node.query.staking.historical_info(1)


def test_params(val_node: Sdk):
    query_resp = val_node.query.staking.params()
    dict_keys_must_match(
        query_resp["params"],
        [
            "unbonding_time",
            "max_entries",
            "max_validators",
            "historical_entries",
            "bond_denom"
        ]
    )

def test_redelegations(val_node: Sdk):
    query_resp = val_node.query.staking.redelegations(
        val_node.address, get_validator_operator_address(val_node)
    )
    a = 1


def test_validators(val_node: Sdk):
    query_resp = val_node.query.staking.validators()
    dict_keys_must_match(
        query_resp,
        ["validators", "pagination"]
    )
    assert query_resp["pagination"]["total"] > 0
    assert len(query_resp["validators"]) > 0
    dict_keys_must_match(
        query_resp["validators"][0],
        [
            "operator_address",
            "consensus_pubkey",
            "jailed",
            "status",
            "tokens",
            "delegator_shares",
            "description",
            "unbonding_height",
            "unbonding_time",
            "commission",
            "min_self_delegation",
        ]
    )


def test_validator(val_node: Sdk):
    validator = val_node.query.staking.validators()["validators"][0]
    query_resp = val_node.query.staking.validator(validator["operator_address"])

    dict_keys_must_match(
        query_resp["validator"],
        [
            "operator_address",
            "consensus_pubkey",
            "jailed",
            "status",
            "tokens",
            "delegator_shares",
            "description",
            "unbonding_height",
            "unbonding_time",
            "commission",
            "min_self_delegation",
        ]
    )
