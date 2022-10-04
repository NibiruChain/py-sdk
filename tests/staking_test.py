import time

import pytest

from nibiru import Network, Sdk
from nibiru.event_specs import EventCaptured, EventType
from nibiru.exceptions import QueryError, SimulationError
from nibiru.msg import MsgDelegate
from nibiru.msg.bank import MsgUndelegate
from nibiru.websocket import NibiruWebsocket
from tests import dict_keys_must_match, transaction_must_succeed


def get_validator_operator_address(val_node: Sdk):
    """
    Return the first validator and delegator
    """
    validator = val_node.query.staking.validators()["validators"][0]
    return validator["operator_address"]


def delegate(val_node: Sdk):
    return val_node.tx.execute_msgs(
        [
            MsgDelegate(
                delegator_address=val_node.address,
                validator_address=get_validator_operator_address(val_node),
                amount=1,
            ),
        ]
    )


def undelegate(val_node: Sdk):
    return val_node.tx.execute_msgs(
        [
            MsgUndelegate(
                delegator_address=val_node.address,
                validator_address=get_validator_operator_address(val_node),
                amount=1,
            ),
        ]
    )


def test_query_vpool(val_node: Sdk):
    query_resp = val_node.query.staking.pool()
    assert query_resp["pool"]["bonded_tokens"] >= 0
    assert query_resp["pool"]["not_bonded_tokens"] >= 0


def test_query_delegation(val_node: Sdk):
    transaction_must_succeed(delegate(val_node))
    query_resp = val_node.query.staking.delegation(
        val_node.address, get_validator_operator_address(val_node)
    )
    dict_keys_must_match(
        query_resp["delegation_response"],
        [
            "delegation",
            "balance",
        ],
    )


def test_query_delegations(val_node: Sdk):
    transaction_must_succeed(delegate(val_node))
    query_resp = val_node.query.staking.delegations(val_node.address)
    dict_keys_must_match(
        query_resp["delegation_responses"][0],
        [
            "delegation",
            "balance",
        ],
    )


def test_query_delegations_to(val_node: Sdk):
    transaction_must_succeed(delegate(val_node))
    query_resp = val_node.query.staking.delegations_to(
        get_validator_operator_address(val_node)
    )
    dict_keys_must_match(
        query_resp["delegation_responses"][0],
        [
            "delegation",
            "balance",
        ],
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
            "bond_denom",
        ],
    )


def test_redelegations(val_node: Sdk):
    query_resp = val_node.query.staking.redelegations(
        val_node.address, get_validator_operator_address(val_node)
    )
    dict_keys_must_match(query_resp, ["redelegation_responses", "pagination"])


def test_unbonding_delegation(val_node: Sdk):
    transaction_must_succeed(delegate(val_node))
    try:
        undelegate(val_node)
    except SimulationError as ex:
        assert "too many unbonding" in ex.args[0]

    query_resp = val_node.query.staking.unbonding_delegation(
        val_node.address, get_validator_operator_address(val_node)
    )
    if query_resp:
        dict_keys_must_match(
            query_resp["unbond"], ["delegator_address", "validator_address", "entries"]
        )
        assert len(query_resp["unbond"]["entries"]) > 0


def test_unbonding_delegations(val_node: Sdk):
    transaction_must_succeed(delegate(val_node))
    try:
        undelegate(val_node)
    except SimulationError as ex:
        assert "too many unbonding" in ex.args[0]

    query_resp = val_node.query.staking.unbonding_delegations(val_node.address)
    dict_keys_must_match(query_resp, ["unbonding_responses", "pagination"])
    dict_keys_must_match(
        query_resp["unbonding_responses"][0],
        ["delegator_address", "validator_address", "entries"],
    )
    assert len(query_resp["unbonding_responses"][0]["entries"]) > 0


def test_unbonding_delegations_from(val_node: Sdk):
    transaction_must_succeed(delegate(val_node))
    try:
        undelegate(val_node)
    except SimulationError as ex:
        assert "too many unbonding" in ex.args[0]

    query_resp = val_node.query.staking.unbonding_delegations_from(
        get_validator_operator_address(val_node)
    )
    dict_keys_must_match(query_resp, ["unbonding_responses", "pagination"])
    dict_keys_must_match(
        query_resp["unbonding_responses"][0],
        ["delegator_address", "validator_address", "entries"],
    )
    assert len(query_resp["unbonding_responses"][0]["entries"]) > 0


def test_validators(val_node: Sdk):
    query_resp = val_node.query.staking.validators()
    dict_keys_must_match(query_resp, ["validators", "pagination"])
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
        ],
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
        ],
    )


def test_staking_events(val_node: Sdk, network: Network):
    """
    Check staking events are properly filtered
    """
    expected_events_tx = [EventType.Delegate]
    expected_events = expected_events_tx

    nibiru_websocket = NibiruWebsocket(
        network,
        expected_events,
    )
    nibiru_websocket.start()
    time.sleep(1)

    delegate(val_node)
    time.sleep(5)

    nibiru_websocket.queue.put(None)
    while True:
        event: EventCaptured = nibiru_websocket.queue.get()
        time.sleep(1)

        if event is None:
            break
        elif event.event_type == "delegate":
            return  # Event Captured! Success

    assert False, "Message delegate not captured"
