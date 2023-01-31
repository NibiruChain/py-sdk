import time

from nibiru import Msg, Network, Sdk
from nibiru.event_specs import EventCaptured, EventType
from nibiru.exceptions import QueryError, SimulationError
from nibiru.websocket import NibiruWebsocket
from tests import dict_keys_must_match, transaction_must_succeed


def get_validator_operator_address(sdk_val: Sdk):
    """
    Return the first validator and delegator
    """
    validator = sdk_val.query.staking.validators()["validators"][0]
    return validator["operator_address"]


def delegate(sdk_val: Sdk):
    return sdk_val.tx.execute_msgs(
        [
            Msg.staking.delegate(
                delegator_address=sdk_val.address,
                validator_address=get_validator_operator_address(sdk_val),
                amount=1,
            ),
        ],
        True,
    )


def undelegate(sdk_val: Sdk):
    return sdk_val.tx.execute_msgs(
        [
            Msg.staking.undelegate(
                delegator_address=sdk_val.address,
                validator_address=get_validator_operator_address(sdk_val),
                amount=1,
            ),
        ],
        True,
    )


def test_query_vpool(sdk_val: Sdk):
    query_resp = sdk_val.query.staking.pool()
    assert query_resp["pool"]["bonded_tokens"] >= 0
    assert query_resp["pool"]["not_bonded_tokens"] >= 0


def test_query_delegation(sdk_val: Sdk):
    transaction_must_succeed(delegate(sdk_val))
    query_resp = sdk_val.query.staking.delegation(
        sdk_val.address, get_validator_operator_address(sdk_val)
    )
    dict_keys_must_match(
        query_resp["delegation_response"],
        [
            "delegation",
            "balance",
        ],
    )


def test_query_delegations(sdk_val: Sdk):
    transaction_must_succeed(delegate(sdk_val))
    query_resp = sdk_val.query.staking.delegations(sdk_val.address)
    dict_keys_must_match(
        query_resp["delegation_responses"][0],
        [
            "delegation",
            "balance",
        ],
    )


def test_query_delegations_to(sdk_val: Sdk):
    transaction_must_succeed(delegate(sdk_val))
    query_resp = sdk_val.query.staking.delegations_to(
        get_validator_operator_address(sdk_val)
    )
    dict_keys_must_match(
        query_resp["delegation_responses"][0],
        [
            "delegation",
            "balance",
        ],
    )


def test_historical_info(sdk_val: Sdk):
    try:
        hist_info = sdk_val.query.staking.historical_info(1)
        if hist_info["hist"]["valset"]:
            dict_keys_must_match(
                hist_info["hist"]["valset"][0],
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
    except QueryError:
        pass


def test_params(sdk_val: Sdk):
    query_resp = sdk_val.query.staking.params()
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


def test_redelegations(sdk_val: Sdk):
    query_resp = sdk_val.query.staking.redelegations(
        sdk_val.address, get_validator_operator_address(sdk_val)
    )
    dict_keys_must_match(query_resp, ["redelegation_responses", "pagination"])


def test_unbonding_delegation(sdk_val: Sdk):
    transaction_must_succeed(delegate(sdk_val))
    try:
        undelegate(sdk_val)
    except SimulationError as ex:
        assert "too many unbonding" in ex.args[0]

    query_resp = sdk_val.query.staking.unbonding_delegation(
        sdk_val.address, get_validator_operator_address(sdk_val)
    )
    if query_resp:
        dict_keys_must_match(
            query_resp["unbond"], ["delegator_address", "validator_address", "entries"]
        )
        assert len(query_resp["unbond"]["entries"]) > 0


def test_unbonding_delegations(sdk_val: Sdk):
    transaction_must_succeed(delegate(sdk_val))
    try:
        undelegate(sdk_val)
    except SimulationError as ex:
        assert "too many unbonding" in ex.args[0]

    query_resp = sdk_val.query.staking.unbonding_delegations(sdk_val.address)
    dict_keys_must_match(query_resp, ["unbonding_responses", "pagination"])
    dict_keys_must_match(
        query_resp["unbonding_responses"][0],
        ["delegator_address", "validator_address", "entries"],
    )
    assert len(query_resp["unbonding_responses"][0]["entries"]) > 0


def test_unbonding_delegations_from(sdk_val: Sdk):
    transaction_must_succeed(delegate(sdk_val))
    try:
        undelegate(sdk_val)
    except SimulationError as ex:
        assert "too many unbonding" in ex.args[0]

    query_resp = sdk_val.query.staking.unbonding_delegations_from(
        get_validator_operator_address(sdk_val)
    )
    dict_keys_must_match(query_resp, ["unbonding_responses", "pagination"])
    dict_keys_must_match(
        query_resp["unbonding_responses"][0],
        ["delegator_address", "validator_address", "entries"],
    )
    assert len(query_resp["unbonding_responses"][0]["entries"]) > 0


def test_validators(sdk_val: Sdk):
    query_resp = sdk_val.query.staking.validators()
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


def test_validator(sdk_val: Sdk):
    validator = sdk_val.query.staking.validators()["validators"][0]
    query_resp = sdk_val.query.staking.validator(validator["operator_address"])

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


def test_staking_events(sdk_val: Sdk, network: Network):
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

    delegate(sdk_val)
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
