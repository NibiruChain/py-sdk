import json
import threading
import time
from multiprocessing import Queue
from typing import List

from websocket import WebSocketApp

from nibiru import Network
from nibiru.event_specs import EventCaptured, Events

ERROR_TIMEOUT_SLEEP = 3


class NibiruWebsocket:
    queue: Queue = None
    captured_events_type: List[List[str]]

    def __init__(
        self, network: Network, captured_events_type: List[Events] = [], verbose=False
    ):
        """
        The nibiru listener provides an interface to easily connect and handle subscription to the events of a nibiru
        chain.
        """

        self.websocket_url = network.websocket_endpoint
        self.captured_events_type: dict = {
            captured_event.value: captured_event
            for captured_event in captured_events_type
        }
        self.queue = Queue()

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
        print("WebSocket starting")
        self._subscribe()

    def _on_error(self, ws: WebSocketApp, error: Exception):
        print(f"Closing websocket, error {error}")
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
        message_time = time.time_ns()
        log = json.loads(message).get("result")
        if log is None:
            return

        events = log.get("events")
        if events is None:
            return

        block_height = log["data"]["value"]["TxResult"]["height"]

        events = json.loads(log["data"]["value"]["TxResult"]["result"]["log"])[0]

        for event in events["events"]:
            if event["type"] in self.captured_events_type:
                event_payload = {
                    attribute["key"]: attribute["value"].strip('"')
                    for attribute in event["attributes"]
                }
                event_payload["block_height"] = block_height
                event_payload["timestamp"] = message_time

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
