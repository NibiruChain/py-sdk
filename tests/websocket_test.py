import time
from datetime import datetime, timedelta
from typing import List

import nibiru
import nibiru.msg
from nibiru import Network, common
from nibiru.event_specs import EventCaptured
from nibiru.websocket import EventType, NibiruWebsocket
from tests import LOGGER


def test_websocket_listen(val_node: nibiru.Sdk, network: Network):
    """
    Open a position and ensure output is correct
    """
    pair = "ubtc:unusd"

    expected_events = [
        # Vpool
        EventType.ReserveSnapshotSavedEvent,
        EventType.SwapQuoteForBaseEvent,
        EventType.SwapBaseForQuoteEvent,
        EventType.MarkPriceChanged,
        # Perp
        EventType.PositionChangedEvent,
        # Bank
        EventType.Transfer,
        # Pricefeed
        EventType.OracleUpdatePriceEvent,
    ]

    nibiru_websocket = NibiruWebsocket(
        network,
        expected_events,
    )
    nibiru_websocket.start()
    time.sleep(1)

    # Open a position from the validator node
    LOGGER.info("Opening position")
    val_node.tx.execute_msgs(
        [
            nibiru.msg.MsgOpenPosition(
                sender=val_node.address,
                token_pair=pair,
                side=common.Side.BUY,
                quote_asset_amount=10,
                leverage=10,
                base_asset_amount_limit=0,
            ),
            nibiru.msg.MsgSend(
                from_address=val_node.address,
                to_address="nibi1a9s5adwysufv4n5ed2ahs4kaqkaf2x3upm2r9p",  # random address
                coins=nibiru.Coin(amount=10, denom="unibi"),
            ),
            nibiru.msg.MsgPostPrice(
                oracle=val_node.address,
                token0="unibi",
                token1="unusd",
                price=10,
                expiry=datetime.utcnow() + timedelta(hours=1),
            ),
        ]
    )

    LOGGER.info("Closing position")
    val_node.tx.execute_msgs(
        nibiru.msg.MsgClosePosition(
            sender=val_node.address,
            token_pair=pair,
        )
    )

    # Give time for events to come
    LOGGER.info("Sent txs, waiting for websocket to pick it up")
    time.sleep(1)

    nibiru_websocket.queue.put(None)
    events: List[EventCaptured] = []
    event = 1
    while True:
        event = nibiru_websocket.queue.get()
        if event is None:
            break
        events.append(event)

    # Asserting for truth because test are running in parallel in the same chain and might result in
    # duplication of markpricechanged events.

    received_events = [event.event_type for event in events]
    assert all(
        [event.get_full_path() in received_events for event in expected_events]
    ), f"Missing events: {[event for event in map(lambda x: x.get_full_path(), expected_events) if event not in received_events]}"
