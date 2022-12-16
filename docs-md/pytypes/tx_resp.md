Module nibiru.pytypes.tx_resp
=============================

Classes
-------

`RawTxResp(*args, **kwargs)`
:   Proxy for a 'TypedDict' representing a transaction response.
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

    ### Ancestors (in MRO)

    * builtins.dict

`TxResp(height: int, txhash: str, data: str, rawLog: List[nibiru.pytypes.event.TxLogEvents], logs: list, gasWanted: int, gasUsed: int, events: list, _raw: RawTxResp)`
:   A 'TxResp' represents the response payload from a successful transaction.

    The 'TxResponse' type is defined in [cosmos-sdk/types/abci.pb.go](https://github.com/cosmos/cosmos-sdk/blob/v0.45.10/types/abci.pb.go)

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

    ### Class variables

    `data: str`
    :

    `events: list`
    :

    `gasUsed: int`
    :

    `gasWanted: int`
    :

    `height: int`
    :

    `logs: list`
    :

    `rawLog: List[nibiru.pytypes.event.TxLogEvents]`
    :

    `txhash: str`
    :

    ### Static methods

    `from_raw(raw_tx_resp: RawTxResp) ‑> nibiru.pytypes.tx_resp.TxResp`
    :
