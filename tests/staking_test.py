from nibiru import Sdk
from tests import dict_keys_must_match


def test_query_vpool(val_node: Sdk):
    query_resp = val_node.query.staking.pool()
    assert query_resp["pool"]["bonded_tokens"] >= 0
    assert query_resp["pool"]["not_bonded_tokens"] >= 0


def test_query_delegation(val_node: Sdk):
    query_resp = val_node.query.staking.delegation(
        'nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl',
        'nibivaloper1zaavvzxez0elundtn32qnk9lkm8kmcszuwx9jz')
    print(query_resp)


def test_query_delegations(val_node: Sdk):
    query_resp = val_node.query.staking.delegations(
        'nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl')
    print(query_resp)


def test_query_delegations_to(val_node: Sdk):
    query_resp = val_node.query.staking.delegations_to(
        'nibivaloper1zaavvzxez0elundtn32qnk9lkm8kmcszuwx9jz')
    print(query_resp)


def test_historical_info(val_node: Sdk):
    query_resp = val_node.query.staking.historical_info(1000)
    print(query_resp)


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

def test_validators(val_node: Sdk):
    query_resp = val_node.query.staking.validators()
    print(query_resp)
