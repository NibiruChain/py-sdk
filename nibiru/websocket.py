import json
import threading
import time
from multiprocessing import Queue
from typing import List

import google.protobuf.json_format
import google.protobuf.message
from websocket import WebSocketApp

import nibiru.query_clients.util
from nibiru import Network
from nibiru.event_specs import EventCaptured, EventType
from nibiru.utils import clean_nested_dict, init_logger

ERROR_TIMEOUT_SLEEP = 3


class NibiruWebsocket:
    queue: Queue = None
    captured_events_type: List[List[str]]

    def __init__(
        self,
        network: Network,
        captured_events_type: List[EventType] = [],
    ):
        """
        The nibiru listener provides an interface to easily connect and handle subscription to the events of a nibiru
        chain.
        """

        self.websocket_url = network.websocket_endpoint
        if self.websocket_url is None:
            raise ValueError(
                "No websocket endpoint provided. Construct the network object setting up the "
                "`websocket_endpoint` endpoint"
            )

        # We use a dictionary for faster search
        self.captured_events_type: dict[str, EventType] = {
            captured_event.get_full_path(): captured_event
            for captured_event in captured_events_type
        }
        self.queue = Queue()
        self.logger = init_logger("ws-logger")

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
        log = json.loads(message).get("result")
        if log is None:
            return

        events = log.get("events")
        if events is None:
            return

        block_height = int(log["data"]["value"]["TxResult"]["height"])
        tx_hash = events["tx.hash"][0]

        events = json.loads(log["data"]["value"]["TxResult"]["result"]["log"])[0]

        for event in events["events"]:
            # This below is faster since self.captured_events_type.keys() are hashed
            if event["type"] in self.captured_events_type:
                event_payload = {
                    attribute["key"]: attribute["value"].strip('"')
                    for attribute in event["attributes"]
                }

                if not isinstance(
                    self.captured_events_type[event["type"]].value,
                    str,
                ):
                    proto_message = google.protobuf.json_format.Parse(
                        json.dumps(clean_nested_dict(event_payload)),
                        self.captured_events_type[event["type"]].value(),
                        ignore_unknown_fields=True,
                    )

                    event_payload = nibiru.query_clients.util.deserialize(
                        proto_message,
                        no_sdk_transformation=True,
                    )

                event_payload["block_height"] = block_height
                event_payload["tx_hash"] = tx_hash

                self.queue.put(EventCaptured(event["type"], event_payload))

    def _subscribe(self):
        self._ws.send(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "subscribe",
                    "id": 1,
                    "params": {"query": "tm.event='Tx'"},
                }
            )
        )
