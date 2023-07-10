import collections
import pprint
from typing import Dict, List


class RawEvent(collections.abc.MutableMapping):
    """Dictionary representing a Tendermint event. In the raw TxOutput of a
    successful transaction, it's the value at

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


class Event:
    """A Tendermint event. An event contains a type and set of attributes.
    Events allow application developers to attach additional information to the
    'ResponseBeginBlock', 'ResponseEndBlock', 'ResponseCheckTx', and 'ResponseDeliverTx'
    functions in the ABCI (application blockchain interface).

    In the Tendermint protobuf, the hard definition is:

    ```proto
    message Event {
      string type = 1;
      repeated EventAttribute attributes = 2;
    }
    message EventAttribute {
      bytes key = 1;
      bytes value = 2;
      bool index = 3;
    }
    ```

    - Ref: [cosmos-sdk/types/events.go](https://github.com/cosmos/cosmos-sdk/blob/93abfdd21d9892550da315b10308519b43fb1775/types/events.go#L221)
    - Ref: [tendermint/tendermint/proto/tendermint/abci/types.proto](https://github.com/tendermint/tendermint/blob/a6dd0d270abc3c01f223eedee44d8b285ae273f6/proto/tendermint/abci/types.proto)
    """

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
        """
        Returns as dictionary

        Returns:
            Dict[str, Dict[str, str]]: the dictionary

        """
        return {self.type: self.attrs}


class TxLogEvents:
    """An element of 'TxResp.rawLog'. This object contains events and messages.

    Keys (KeyType):
        type (str)
        attributes (List[EventAttribute])

    Args:
        events_raw (List[RawEvent])

    Attributes:
        events (List[Event])
        msgs (List[str])
        events_raw (List[RawEvent])
        event_types (List[str])
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
        """
        Returns the message types as a list of strings.

        Returns:
            List[str]: the list of msg types as strings

        """
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
