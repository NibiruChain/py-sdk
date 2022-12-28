import dataclasses
from typing import Any, Dict, List, Union

from nibiru import utils
from nibiru.pytypes import event


@dataclasses.dataclass
class TxResp:
    """
    A 'TxResp' represents the response payload from a successful transaction.

    The 'TxResponse' type is defined in
    [cosmos-sdk/types/abci.pb.go](https://github.com/cosmos/cosmos-sdk/blob/v0.45.10/types/abci.pb.go)

    ### Args & Attributes:

    - height (int): block height at which the transaction was committed.
    - txhash (str): unique identifier for the transaction
    - data (str): Result bytes.
    - rawLog (List[TxLogEvents]): Raw output of the SDK application's logger.
        Possibly non-deterministic. This output also contains the events emitted
        during the processing of the transaction, which is equivalently
    - logs (list): Typed output of the SDK application's logger.
        Possibly non-deterministic.
    - gasWanted (str): Amount of gas units requested for the transaction.
    - gasUsed (str): Amount of gas units consumed by the transaction execution.
    - events (list): Tendermint events emitted by processing the transaction.
        The events in this attribute include those emitted by both from
        the ante handler and the processing of all messages, whereas the
        'rawLog' events are only those emitted when processing messages (with
        additional metadata).
    - _raw (RawTxResp): The unprocessed form of the transaction resposnse.

    """

    height: int
    txhash: str
    data: str
    rawLog: List[event.TxLogEvents]
    logs: list
    gasWanted: int
    gasUsed: int
    events: list
    _raw: 'RawTxResp'

    @classmethod
    def from_raw(cls, raw_tx_resp: 'RawTxResp') -> 'TxResp':
        return cls(
            height=int(raw_tx_resp["height"]),
            txhash=raw_tx_resp["txhash"],
            data=raw_tx_resp["data"],
            rawLog=[
                event.TxLogEvents(msg_log['events'])
                for msg_log in raw_tx_resp["rawLog"]
            ],
            logs=raw_tx_resp["logs"],
            gasWanted=int(raw_tx_resp["gasWanted"]),
            gasUsed=int(raw_tx_resp["gasUsed"]),
            events=raw_tx_resp["events"],
            _raw=raw_tx_resp,
        )

    def __repr__(self) -> str:
        repr_body = ", ".join(
            [
                f"height={self.height}",
                f"txhash={self.txhash}",
                f"gasUsed={self.gasUsed}",
                f"gasWanted={self.gasWanted}",
                f"rawLog={self.rawLog}",
            ]
        )
        return f"TxResp({repr_body})"


# from typing import TypedDict  # not available in Python 3.7
# class RawTxResp(TypedDict):
class RawTxResp(dict):
    """Proxy for a 'TypedDict' representing a transaction response.
    - The 'TxResponse' type is defined in
    [cosmos-sdk/types/abci.pb.go](https://github.com/cosmos/cosmos-sdk/blob/v0.45.10/types/abci.pb.go)

    ### Keys (ValueType):

    - height (str): block height at which the transaction was committed.
    - txhash (str): unique identifier for the transaction
    - data (str): Result bytes.
    - rawLog (list): Raw output of the SDK application's logger.
        Possibly non-deterministic. This output also contains the events emitted
        during the processing of the transaction, which is equivalently
    - logs (list): Typed output of the SDK application's logger.
        Possibly non-deterministic.
    - gasWanted (str): Amount of gas units requested for the transaction.
    - gasUsed (str): Amount of gas units consumed by the transaction execution.
    - events (list): Tendermint events emitted by processing the transaction.
        The events in this attribute include those emitted by both from
        the ante handler and the processing of all messages, whereas the
        'rawLog' events are only those emitted when processing messages (with
        additional metadata).
    """

    def __new__(cls, _dict: Dict[str, Any]) -> Dict[str, Union[str, list]]:
        """Verifies that the dictionary has the expected keys."""
        keys_wanted = ["height", "txhash", "data", "rawLog", "logs"] + [
            "gasWanted",
            "gasUsed",
            "events",
        ]
        utils.dict_keys_must_match(_dict, keys_wanted)
        return _dict
