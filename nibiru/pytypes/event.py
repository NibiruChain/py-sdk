import collections
import pprint
from typing import Dict, List


class RawEvent(collections.abc.MutableMapping):
    """Dictionary representing a Tendermint event. In the raw TxOutput of a
    successful transaciton, it's the value at
    ```python
    tx_output['rawLog'][0]['events']
    ```

    ### Keys (KeyType):
    - attributes (List[Dict[str,str]])
    - type (str)

    ### Example:
    ```python
    {'attributes': [
        {'key': 'recipient', 'value': 'nibi1uvu52rxwqj5ndmm59y6atvx33mru9xrz6sqekr'},
        {'key': 'sender', 'value': 'nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl'},
        {'key': 'amount', 'value': '7unibi,70unusd'}],
    'type': 'transfer'}
    ```
    """


# TODO test conversions from RawEvent to Event
class Event:
    type: str
    attrs: Dict[str, str]

    def __init__(self, raw_event: RawEvent):
        self.type = raw_event["type"]
        self.attrs = self.parse_attributes(raw_event["attributes"])

    @staticmethod
    def parse_attributes(raw_attributes: List[Dict[str, str]]) -> Dict[str, str]:
        try:
            attributes: dict[str, str] = {
                kv_dict['key']: kv_dict['value'] for kv_dict in raw_attributes
            }
            return attributes
        except:
            raise Exception(
                f"failed to parse raw attributes:\n{pprint.pformat(raw_attributes)}"
            )

    def __repr__(self) -> str:
        return f"Event(type={self.type}, attrs={self.attrs})"

    def to_dict(self) -> Dict[str, Dict[str, str]]:
        return {self.type: self.attrs}


class TxLogEvents:
    """A dictionary corresponding to a Tendermint event

    Keys (KeyType):
        type (str)
        attributes (List[EventAttribute])
    """

    events: List[Event]
    msgs: List[str]
    events_raw: List[RawEvent]
    event_types: List[str]

    def __init__(self, events_raw: List[RawEvent] = []):
        self.events_raw = events_raw
        self.events = [Event(raw_event) for raw_event in events_raw]
        self.msgs = self.get_msg_types()

    def get_msg_types(self) -> List[str]:

        msgs = []
        self.event_types = []
        for event in self.events:
            self.event_types.append(event.type)
            if event.type == "message":
                msgs.append(event.attrs["action"])
        return msgs

    def __repr__(self) -> str:
        self_as_dict = dict(msgs=self.msgs, events=[e.to_dict() for e in self.events])
        return pprint.pformat(self_as_dict, indent=2)
