import multiprocessing as mp
import time
from typing import List

import pytest

import pysdk
import tests
from pysdk import Msg, Network, event_specs
from pysdk import websocket as ws


@pytest.mark.slow
def test_websocket_listen(sdk_val: pysdk.Sdk, network: Network):
    """Open a position and ensure output is correct"""
    pair = "ubtc:unusd"

    expected_events_tx = [
        # Perp
        ws.EventType.PositionChangedEvent,
        # Bank
        ws.EventType.Transfer,
    ]

    expected_events = expected_events_tx

    websocket = ws.NibiruWebsocket(
        network,
        expected_events,
    )
    websocket.start()
    time.sleep(1)

    # Open a position from the validator node
    tests.LOGGER.info("Opening position")
    random_address: str = "nibi1a9s5adwysufv4n5ed2ahs4kaqkaf2x3upm2r9p"
    sdk_val.tx.execute_msgs(
        [
            Msg.perp.open_position(
                sender=sdk_val.address,
                pair=pair,
                is_long=True,
                quote_asset_amount=10,
                leverage=10,
                base_asset_amount_limit=0,
            ),
            Msg.bank.send(
                from_address=sdk_val.address,
                to_address=random_address,
                coins=pysdk.Coin(amount=10, denom="unibi"),
            ),
        ]
    )

    tests.LOGGER.info("Closing position")
    sdk_val.tx.execute_msgs(
        Msg.perp.close_position(
            sender=sdk_val.address,
            pair=pair,
        )
    )

    # Give time for events to come
    tests.LOGGER.info("Sent txs, waiting for websocket to pick it up")
    time.sleep(3)

    websocket.queue.put(None)
    events: List[event_specs.EventCaptured] = []
    while True:
        event: event_specs.EventCaptured = websocket.queue.get()
        if event is None:
            break
        events.append(event)

        # Asserting for truth because test are running in parallel in the same
        # chain and might result in duplication of markpricechanged events.

        received_events: List[event_specs.EventType] = [
            event.event_type for event in events
        ]

        missing_events = [
            event
            for event in map(lambda x: x.get_full_path(), expected_events)
            if event not in received_events
        ]

        assert not missing_events, f"Missing events: {missing_events}"


@pytest.mark.slow
def test_websocket_tx_fail_queue(sdk_val: pysdk.Sdk, network: Network):
    """
    Try executing failing TXs and get errors from tx_fail_queue
    """
    tx_fail_queue: mp.Queue = mp.Queue()

    websocket = ws.NibiruWebsocket(
        network,
        [ws.EventType.PositionChangedEvent],
        tx_fail_queue,
    )
    websocket.start()
    time.sleep(1)

    # Send failing closing transaction without simulation
    sdk_val.tx.client.sync_timeout_height()
    address = sdk_val.tx.ensure_address_info()
    tx = (
        pysdk.Transaction()
        .with_messages(
            [
                Msg.perp.close_position(
                    sender=sdk_val.address,
                    pair="abc:def",
                ).to_pb()
            ]
        )
        .with_sequence(address.get_sequence())
        .with_account_num(address.get_number())
        .with_chain_id(network.chain_id)
        .with_signer(sdk_val.tx.priv_key)
    )
    sdk_val.tx.execute_tx(tx, gas_estimate=300000)

    time.sleep(3)

    tx_fail_queue.put(None)
    fail_event_found = False

    while True:
        event = tx_fail_queue.get()
        if event is None:
            break
        if "failed to execute message" in event["error"]:
            fail_event_found = True
            break

    breakpoint()
    assert fail_event_found, "Transaction failure not captured"
