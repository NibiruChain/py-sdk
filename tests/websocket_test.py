import time
from datetime import datetime, timedelta
from multiprocessing import Queue
from typing import List

import pytest

import nibiru
from nibiru import Msg, Network, Sdk, Transaction
from nibiru.event_specs import EventCaptured
from nibiru.websocket import EventType, NibiruWebsocket
from tests import LOGGER


@pytest.mark.slow
def test_websocket_listen(
    sdk_val: nibiru.Sdk,  network: Network
):
    """
    Open a position and ensure output is correct
    """
    pair = "ubtc:unusd"

    expected_events_tx = [
        # Vpool
        EventType.SwapOnVpoolEvent,
        EventType.MarkPriceChanged,
        # Perp
        EventType.PositionChangedEvent,
        # Bank
        EventType.Transfer,
    ]

    expected_events = expected_events_tx

    nibiru_websocket = NibiruWebsocket(
        network,
        expected_events,
    )
    nibiru_websocket.start()
    time.sleep(1)

    # Open a position from the validator node
    LOGGER.info("Opening position")
    sdk_val.tx.execute_msgs(
        [
            Msg.perp.open_position(
                sender=sdk_val.address,
                token_pair=pair,
                is_long=True,
                quote_asset_amount=10,
                leverage=10,
                base_asset_amount_limit=0,
            ),
            Msg.bank.send(
                from_address=sdk_val.address,
                to_address="nibi1a9s5adwysufv4n5ed2ahs4kaqkaf2x3upm2r9p",  # random address
                coins=nibiru.Coin(amount=10, denom="unibi"),
            ),
        ]
    )

    LOGGER.info("Closing position")
    sdk_val.tx.execute_msgs(
        Msg.perp.close_position(
            sender=sdk_val.address,
            token_pair=pair,
        )
    )

    # Give time for events to come
    LOGGER.info("Sent txs, waiting for websocket to pick it up")
    time.sleep(3)

    nibiru_websocket.queue.put(None)
    events: List[EventCaptured] = []
    while True:
        event = nibiru_websocket.queue.get()
        if event is None:
            break
        events.append(event)

    # Asserting for truth because test are running in parallel in the same chain and might result in
    # duplication of markpricechanged events.

    received_events = [event.event_type for event in events]

    missing_events = [
        event
        for event in map(lambda x: x.get_full_path(), expected_events)
        if event not in received_events
    ]

    assert not missing_events, f"Missing events: {missing_events}"


@pytest.mark.slow
def test_websocket_tx_fail_queue(sdk_val: Sdk, network: Network):
    """
    Try executing failing TXs and get errors from tx_fail_queue
    """
    tx_fail_queue = Queue()

    nibiru_websocket = NibiruWebsocket(
        network,
        [EventType.PositionChangedEvent],
        tx_fail_queue,
    )
    nibiru_websocket.start()
    time.sleep(1)

    # Send failing closing transaction without simulation
    sdk_val.tx.client.sync_timeout_height()
    address = sdk_val.tx.get_address_info()
    tx = (
        Transaction()
        .with_messages(
            [
                Msg.perp.close_position(
                    sender=sdk_val.address,
                    token_pair="abc:def",
                ).to_pb()
            ]
        )
        .with_sequence(address.get_sequence())
        .with_account_num(address.get_number())
        .with_chain_id(network.chain_id)
        .with_signer(sdk_val.tx.priv_key)
    )
    sdk_val.tx.execute_tx(tx, 300000)

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

    assert fail_event_found, "Transaction failure not captured"
