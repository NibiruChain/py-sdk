import abc
import collections.abc
import dataclasses
import pprint
from enum import Enum
from typing import Dict, List

from nibiru_proto.proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb
from nibiru_proto.proto.dex.v1.pool_pb2 import PoolType  # noqa

import nibiru

MAX_MEMO_CHARACTERS = 256
GAS_PRICE = 1 * pow(10, -3)


class TxType(Enum):
    """
    The TxType allows you to chose what type of synchronization you want to use to send transaction
    """

    SYNC = 1
    """
    The CLI waits for a CheckTx execution response only.
    Each full-node that receives a transaction sends a CheckTx to the application layer to check for validity, and
    receives an abci.ResponseCheckTx. If the Tx passes the checks, it is held in the nodes' Mempool , an in-memory pool
    of transactions unique to each node pending inclusion in a block - honest nodes will discard Tx if it is found to
    be invalid.

    Prior to consensus, nodes continuously check incoming transactions and gossip them to their peers.
    """

    ASYNC = 2
    """
    The CLI returns immediately (transaction might fail silently).
    If you send a transaction with this option, it is recommended to query the transaction output using the hash of the
    transaction given by the output of the tx call.
    """

    BLOCK = 3
    """
    The tx function will wait unitl the tx is be committed in a block.
    This have the effect of having the full log of the transaction available with the output of the method. These logs
    will include information as to coin sent and received, states changed etc.
    """


class Side(Enum):
    BUY = 1
    SELL = 2


class Direction(Enum):
    ADD = 1
    REMOVE = 2


@dataclasses.dataclass
class Coin:
    amount: float
    denom: str

    def _generate_proto_object(self):
        return cosmos_base_coin_pb.Coin(amount=str(self.amount), denom=self.denom)


@dataclasses.dataclass
class PoolAsset:
    token: Coin
    weight: float


class TxConfig:
    def __init__(
        self,
        gas_wanted: int = 0,
        gas_multiplier: float = 1.25,
        gas_price: float = 0.25,
        tx_type: TxType = TxType.ASYNC,
    ):
        """
        The TxConfig object allows to customize the behavior of the Sdk interface when a transaction is sent.

        Args:
            gas_wanted (int, optional): Set the absolute gas_wanted to be used.
                Defaults to 0.
            gas_multiplier (float, optional): Set the gas multiplier that's being
                applied to the estimated gas. If gas_wanted is set, this property
                is ignored. Defaults to 0.
            gas_price (float, optional): Set the gas price used to calculate the fee.
                Defaults to 0.25.
            tx_type (TxType, optional): Configure how to execute the tx. Defaults to TxType.ASYNC.
        """

        self.gas_multiplier = gas_multiplier
        self.gas_wanted = gas_wanted
        self.gas_price = gas_price
        self.tx_type = tx_type


class PythonMsg(abc.ABC):
    @abc.abstractmethod
    def to_pb(self) -> nibiru.ProtobufMessage:
        """
        Generate the protobuf message

        Returns:
            Any: The protobuff mesage
        """


@dataclasses.dataclass
class TxResp:
    """
    A 'TxResp' represents the response payload from a successful transaction.

    Args & Attributes:
        height (str): ...TODO
        txhash (str): ...TODO
        data (str): ...TODO
        rawLog (list): ...TODO
        logs (list): ...TODO
        gasWanted (str): ...TODO
        gasUsed (str): ...TODO
        events (list): ...TODO

    """

    height: str
    txhash: str
    data: str
    rawLog: list
    logs: list
    gasWanted: str
    gasUsed: str
    events: list


class RawEvent(collections.abc.MutableMapping):
    """Dictionary representing a Tendermint event. In the raw TxOutput of a
    successful transaciton, it's the value at
    ```python
    tx_output['rawLog'][0]['events']
    ```

    Keys (KeyType):
        attributes (List[Dict[str,str]])
        type (str)

    Example:
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
    event_type: str
    attributes: Dict[str, str]

    def __init__(self, raw_event: RawEvent):
        self.event_type = raw_event["type"]
        self.attributes = self.parse_attributes(raw_event["attributes"])

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


class RawLogEvents:
    """A dictionary corresponding to a Tendermint event

    Keys (KeyType):
        type (str)
        attributes (List[EventAttribute])
    """

    events_raw: List[RawEvent]

    def __init__(self, events_raw: List[RawEvent] = []):
        self.events_raw = events_raw

    # events_raw: list[]
