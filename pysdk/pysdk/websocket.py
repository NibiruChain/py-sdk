import base64
import dataclasses
import json
import logging
import threading
import time
from dataclasses import field
from json import JSONDecodeError
from multiprocessing import Queue
from typing import Any, Callable, Dict, List, Optional

import google.protobuf.json_format
import google.protobuf.message
from websocket import WebSocketApp

import pysdk.query_clients.util
from pysdk import Network
from pysdk.event_specs import EventCaptured, EventType
from pysdk.utils import clean_nested_dict

ERROR_TIMEOUT_SLEEP = 3


@dataclasses.dataclass
class NibiruWebsocket:
    network: Network
    captured_event_types: List[EventType] = field(default_factory=list)
    queue: Queue = Queue()
    tx_fail_queue: Queue = Queue()
    captured_event_types_map: Dict[str, EventType] = field(default_factory=dict)
    logger: logging.Logger = logging.getLogger("ws-logger")

    def __post_init__(self):
        """
        The nibiru listener provides an interface to easily connect and handle subscription to the events of a nibiru
        chain.
        """

        self.websocket_url = self.network.websocket_endpoint
        if self.websocket_url is None:
            raise ValueError(
                f"No websocket endpoint provided for network {self.network}."
                + "\nConstruct the network object with a valid `websocket_endpoint`"
            )

        # We use a dictionary for faster search
        self.captured_event_types_map: dict[str, EventType] = {
            captured_event.get_full_path(): captured_event
            for captured_event in self.captured_event_types
        }

    def start(self):
        """
        Start the websocket and fill the queue with events.
        """

        self._ws = WebSocketApp(
            self.websocket_url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
        )
        threading.Thread(
            target=self._ws.run_forever,
            daemon=True,
            name=f"Nibiru websocket @ {self.websocket_url}",
        ).start()

    def _on_open(self, _: WebSocketApp):
        self.logger.info("WebSocket starting")
        self._subscribe()

    def _on_error(self, ws: WebSocketApp, error: Exception):
        self.logger.error(f"Closing websocket, error {error}")
        self.logger.exception(error)
        ws.close()
        time.sleep(ERROR_TIMEOUT_SLEEP)
        ws.run_forever()

    def _on_message(self, _: WebSocketApp, message: str):
        """
        Parse the message and filter through them using the captured event type.
        Put these filtered event in the queue.

        Args:
            _ (WebSocketApp): No idea what this is
            message (str): The message in a utf-8 data received from the server
        """
        log = json.loads(message).get("result", {})
        if not log:
            return

        if log["query"] == "tm.event='Tx'":
            self._handle_txs(log)

        if log["query"] == "tm.event='NewBlock'":
            self._handle_block(log)

    def _handle_block(self, log: dict) -> None:
        """
        Read the log for the begin and end block and put relevant events in the queue.

        Args:
            log (dict): The logs
        """

        block_begin_events = log["data"]["value"]["result_begin_block"]["events"]
        block_end_events = log["data"]["value"]["result_end_block"]["events"]

        block_height = log["data"]["value"]["block"]["header"]["height"]

        for event in block_begin_events + block_end_events:
            self._handle_event(
                block_height=block_height, tx_hash=None, event=event, base64_decode=True
            )

    def _handle_txs(self, log: Dict[str, Any]):
        """
        Read the log for each tx in a block and put relevant events in the queue.

        Args:
            log (dict): The logs
        """
        events = log.get("events")
        if events is None:
            return

        block_height = int(log["data"]["value"]["TxResult"]["height"])
        tx_hash = events["tx.hash"][0]

        try:
            events = json.loads(log["data"]["value"]["TxResult"]["result"]["log"])[0]
        except JSONDecodeError as ex:
            # failed to execute message
            raw_log = log["data"]["value"]["TxResult"]["result"]["log"]
            if self.tx_fail_queue:
                self.tx_fail_queue.put(
                    {"block_height": block_height, "tx_hash": tx_hash, "error": raw_log}
                )
            self.logger.debug(f"Failed parsing events log: {raw_log}. {ex}")
            return

        for event in events["events"]:
            self._handle_event(block_height, tx_hash, event)

    def _handle_event(
        self,
        block_height: int,
        tx_hash: Optional[str],
        event: dict,
        base64_decode: bool = False,
    ):
        """
        Read an event and put it in the queue if it's part of the captured event type.

        Args:
            block_height (int): The height of the block
            tx_hash (str): The hash of the transaction if it's coming from a transaction
            event (dict): The event to parse
            base64_decode (bool, optional): Whether to base64 decode the attributes and key of the event.
                Defaults to False.
        """
        # This below is faster since self.captured_events_type.keys() are hashed

        def decode_base64(value: Any) -> str:
            return base64.b64decode(value).decode('utf-8')

        def decode_mock(value: str) -> str:
            return value

        decode_fn: Callable[[Any], str]
        if base64_decode:
            decode_fn = decode_base64
        else:
            decode_fn = decode_mock

        if event["type"] in self.captured_event_types_map:
            event_payload = {
                decode_fn(attribute["key"]): decode_fn(attribute["value"]).strip('"')
                for attribute in event["attributes"]
            }

            if not isinstance(
                self.captured_event_types_map[event["type"]].value,
                str,
            ):
                proto_message = google.protobuf.json_format.Parse(
                    json.dumps(clean_nested_dict(event_payload)),
                    self.captured_event_types_map[event["type"]].value(),
                    ignore_unknown_fields=True,
                )

                event_payload = pysdk.query_clients.util.deserialize(
                    proto_message,
                    no_sdk_transformation=True,
                )

            event_payload["block_height"] = block_height
            event_payload["tx_hash"] = tx_hash

            self.queue.put(EventCaptured(event["type"], event_payload))

    def _subscribe(self):
        tm_events: Dict[str, str] = {
            "new_block_value": "NewBlock",
            "tx_value": "Tx",
        }

        for _, event_name in tm_events.items():
            self._ws.send(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "subscribe",
                        "id": 1,
                        "params": {"query": f"tm.event='{event_name}'"},
                    }
                )
            )
