import abc
import dataclasses
from enum import Enum
from typing import List

from nibiru_proto.cosmos.base.v1beta1 import (  # noqa # type: ignore
    coin_pb2 as cosmos_base_coin_pb,
)
from nibiru_proto.nibiru.spot.v1.pool_pb2 import PoolType  # noqa  # type: ignore

import pysdk

MAX_MEMO_CHARACTERS = 256
DEFAULT_GAS_PRICE = 1 * pow(10, -3)


class TxBroadcastMode(Enum):
    """
    The TxType allows you to choose what type of synchronization you want to
    use to broadcast a transaction.

    ### TxType.SYNC

    The CLI waits for a CheckTx execution response only. Each full-node that
    receives a transaction sends a CheckTx to the application layer to check
    for validity, and receives an abci.ResponseCheckTx. If the Tx passes the
    checks, it is held in the nodes' Mempool , an in-memory pool of
    transactions unique to each node pending inclusion in a block - honest
    nodes will discard Tx if it is found to be invalid.

    Prior to consensus, nodes continuously check incoming transactions and
    gossip them to their peers.

    ### TxType.ASYNC

    The CLI returns immediately (transaction might fail silently). If you send
    a transaction with this option, it is recommended to query the transaction
    output using the hash of the transaction given by the output of the tx
    call.

    ### TxType.BLOCK (Deprecated since Cosmos-SDK v0.47)

    The tx function will wait unitl the tx is be committed in a block. This
    have the effect of having the full log of the transaction available with
    the output of the method. These logs will include information as to coin
    sent and received, states changed etc.
    """

    SYNC = 1

    ASYNC = 2

    BLOCK = 3


class Direction(Enum):
    LONG = 1
    SHORT = 2


@dataclasses.dataclass
class Coin:
    amount: float
    denom: str

    def _generate_proto_object(self):
        """

        Returns:
            cosmos_base_coin_pb.Coin: the coin object as proto object

        """
        return cosmos_base_coin_pb.Coin(amount=str(self.amount), denom=self.denom)


@dataclasses.dataclass
class PoolAsset:
    token: Coin
    weight: float


@dataclasses.dataclass
class TxConfig:
    """
    The TxConfig object allows to customize the behavior of the Sdk interface
    when a transaction is sent.

    Args:
        gas_wanted (int, optional): Set the absolute gas_wanted to be used.
            Defaults to 0.
        gas_multiplier (float, optional): Set the gas multiplier that's being
            applied to the estimated gas. If gas_wanted is set, this property
            is ignored. Defaults to 0.
        gas_price (float, optional): Set the gas price used to calculate the
            gas fee. Defaults to 0.25.
        tx_type (TxType, optional): Configure how to execute the tx.
            Defaults to TxBroadcastMode.SYNC.
    """

    gas_wanted: int = 0
    gas_multiplier: float = 1.25
    gas_price: float = 0.25
    broadcast_mode: TxBroadcastMode = TxBroadcastMode.SYNC


TX_CONFIG_ATTRS: List[str] = [
    "gas_wanted",
    "gas_multiplier",
    "gas_price",
    "tx_type",
]


class PythonMsg(abc.ABC):
    @abc.abstractmethod
    def to_pb(self) -> pysdk.ProtobufMessage:
        """
        Generate the protobuf message

        Returns:
            Any: The protobuff mesage
        """
