import time

import tests
from nibiru import ChainClient, Msg, Network, event_specs, websocket
from nibiru.exceptions import QueryError, SimulationError


def get_validator_operator_address(client_validator: ChainClient):
    """
    Return the first validator and delegator
    """
    validator = client_validator.query.staking.validators()["validators"][0]
    return validator["operator_address"]


def delegate(client_validator: ChainClient):
    return client_validator.tx.execute_msgs(
        [
            Msg.staking.delegate(
                delegator_address=client_validator.address,
                validator_address=get_validator_operator_address(client_validator),
                amount=1,
            ),
        ],
    )


def undelegate(client_validator: ChainClient):
    return client_validator.tx.execute_msgs(
        [
            Msg.staking.undelegate(
                delegator_address=client_validator.address,
                validator_address=get_validator_operator_address(client_validator),
                amount=1,
            ),
        ],
    )


def test_query_vpool(client_validator: ChainClient):
    query_resp = client_validator.query.staking.pool()
    assert query_resp["pool"]["bonded_tokens"] >= 0
    assert query_resp["pool"]["not_bonded_tokens"] >= 0


def test_query_delegation(client_validator: ChainClient):
    tests.broadcast_tx_must_succeed(delegate(client_validator))
    query_resp = client_validator.query.staking.delegation(
        client_validator.address, get_validator_operator_address(client_validator)
    )
    tests.dict_keys_must_match(
        query_resp["delegation_response"],
        [
            "delegation",
            "balance",
        ],
    )


def test_query_delegations(client_validator: ChainClient):
    tests.broadcast_tx_must_succeed(delegate(client_validator))
    query_resp = client_validator.query.staking.delegations(client_validator.address)
    tests.dict_keys_must_match(
        query_resp["delegation_responses"][0],
        [
            "delegation",
            "balance",
        ],
    )


def test_query_delegations_to(client_validator: ChainClient):
    tests.broadcast_tx_must_succeed(delegate(client_validator))
    query_resp = client_validator.query.staking.delegations_to(
        get_validator_operator_address(client_validator)
    )
    tests.dict_keys_must_match(
        query_resp["delegation_responses"][0],
        [
            "delegation",
            "balance",
        ],
    )


def test_historical_info(client_validator: ChainClient):
    try:
        hist_info = client_validator.query.staking.historical_info(1)
        if hist_info["hist"]["valset"]:
            tests.dict_keys_must_match(
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
                    "unbonding_on_hold_ref_count",
                    "unbonding_ids",
                ],
            )
    except QueryError:
        pass


def test_params(client_validator: ChainClient):
    query_resp = client_validator.query.staking.params()
    tests.dict_keys_must_match(
        query_resp["params"],
        [
            "unbonding_time",
            "max_entries",
            "max_validators",
            "historical_entries",
            "bond_denom",
            "min_commission_rate",
        ],
    )


def test_redelegations(client_validator: ChainClient):
    query_resp = client_validator.query.staking.redelegations(
        client_validator.address, get_validator_operator_address(client_validator)
    )
    tests.dict_keys_must_match(query_resp, ["redelegation_responses", "pagination"])


def test_unbonding_delegation(client_validator: ChainClient):
    tests.broadcast_tx_must_succeed(delegate(client_validator))
    try:
        undelegate(client_validator)
        query_resp = client_validator.query.staking.unbonding_delegation(
            client_validator.address, get_validator_operator_address(client_validator)
        )
        if query_resp.get("unbonding_responses"):
            tests.dict_keys_must_match(
                query_resp["unbond"],
                ["delegator_address", "validator_address", "entries"],
            )
            assert len(query_resp["unbond"]["entries"]) > 0

    except BaseException as err:
        tests.raises(
            ok_errs=["too many unbonding", "Error on UnbondingDelegation"], err=err
        )


def test_unbonding_delegations(client_validator: ChainClient):
    tests.broadcast_tx_must_succeed(delegate(client_validator))
    try:
        undelegate(client_validator)
    except SimulationError as ex:
        assert "too many unbonding" in ex.args[0]

    query_resp = client_validator.query.staking.unbonding_delegations(
        client_validator.address
    )

    tests.dict_keys_must_match(query_resp, ["unbonding_responses", "pagination"])
    if query_resp.get("unbonding_responses"):
        tests.dict_keys_must_match(
            query_resp["unbonding_responses"][0],
            ["delegator_address", "validator_address", "entries"],
        )
        assert len(query_resp["unbonding_responses"][0]["entries"]) > 0


def test_unbonding_delegations_from(client_validator: ChainClient):
    tests.broadcast_tx_must_succeed(delegate(client_validator))
    try:
        undelegate(client_validator)
    except SimulationError as ex:
        assert "too many unbonding" in ex.args[0]

    query_resp = client_validator.query.staking.unbonding_delegations_from(
        get_validator_operator_address(client_validator)
    )

    tests.dict_keys_must_match(query_resp, ["unbonding_responses", "pagination"])
    if query_resp.get("unbonding_responses"):
        tests.dict_keys_must_match(
            query_resp["unbonding_responses"][0],
            ["delegator_address", "validator_address", "entries"],
        )
        assert len(query_resp["unbonding_responses"][0]["entries"]) > 0


def test_validators(client_validator: ChainClient):
    query_resp = client_validator.query.staking.validators()
    tests.dict_keys_must_match(query_resp, ["validators", "pagination"])
    assert query_resp["pagination"]["total"] > 0
    assert len(query_resp["validators"]) > 0
    tests.dict_keys_must_match(
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
            "unbonding_on_hold_ref_count",
            "unbonding_ids",
        ],
    )


def test_validator(client_validator: ChainClient):
    validator = client_validator.query.staking.validators()["validators"][0]
    query_resp = client_validator.query.staking.validator(validator["operator_address"])

    tests.dict_keys_must_match(
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
            "unbonding_on_hold_ref_count",
            "unbonding_ids",
        ],
    )


def test_staking_events(client_validator: ChainClient, network: Network):
    """
    Check staking events are properly filtered
    """
    expected_events_tx = [event_specs.EventType.Delegate]
    expected_events = expected_events_tx

    ws = websocket.NibiruWebsocket(
        network,
        expected_events,
    )
    ws.start()
    time.sleep(1)

    delegate(client_validator)
    time.sleep(5)
    success: bool = False
    ws.queue.put(None)
    while True:
        if ws.captured_event_types_map.get("delegate"):
            success = True  # Event Captured! Success
        event: event_specs.EventCaptured = ws.queue.get()
        time.sleep(1)
        if event is None:
            break
        elif event.event_type == "delegate":
            success = True  # Event Captured! Success
    assert success, "Message delegate captured"
