Module pysdk.pytypes.event
==========================

Classes
-------

`Event(raw_event: pysdk.pytypes.event.RawEvent)`
:   A Tendermint event. An event contains a type and set of attributes.
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

    ### Class variables

    `attrs: Dict[str, str]`
    :

    `type: str`
    :

    ### Static methods

    `parse_attributes(raw_attributes: List[Dict[str, str]]) ‑> Dict[str, str]`
    :

    ### Methods

    `to_dict(self) ‑> Dict[str, Dict[str, str]]`
    :   Returns as dictionary

        Returns:
            Dict[str, Dict[str, str]]: the dictionary

`RawEvent()`
:   Dictionary representing a Tendermint event. In the raw TxOutput of a
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

    ### Ancestors (in MRO)

    * collections.abc.MutableMapping
    * collections.abc.Mapping
    * collections.abc.Collection
    * collections.abc.Sized
    * collections.abc.Iterable
    * collections.abc.Container

`TxLogEvents(events_raw: List[pysdk.pytypes.event.RawEvent] = [])`
:   An element of 'TxResp.rawLog'. This object contains events and messages.

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

    ### Class variables

    `event_types: List[str]`
    :

    `events: List[pysdk.pytypes.event.Event]`
    :

    `events_raw: List[pysdk.pytypes.event.RawEvent]`
    :

    `msgs: List[str]`
    :

    ### Methods

    `get_msg_types(self) ‑> List[str]`
    :   Returns the message types as a list of strings.

        Returns:
            List[str]: the list of msg types as strings
