Module pysdk.pytypes.common
===========================

Classes
-------

`Coin(amount: float, denom: str)`
:   Coin(amount: float, denom: str)

    ### Class variables

    `amount: float`
    :

    `denom: str`
    :

`Direction(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `LONG`
    :

    `SHORT`
    :

`PoolAsset(token: pysdk.pytypes.common.Coin, weight: float)`
:   PoolAsset(token: pysdk.pytypes.common.Coin, weight: float)

    ### Class variables

    `token: pysdk.pytypes.common.Coin`
    :

    `weight: float`
    :

`PythonMsg()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * pysdk.msg.bank.MsgSend
    * pysdk.msg.perp.MsgAddMargin
    * pysdk.msg.perp.MsgClosePosition
    * pysdk.msg.perp.MsgMarketOrder
    * pysdk.msg.perp.MsgMultiLiquidate
    * pysdk.msg.perp.MsgRemoveMargin
    * pysdk.msg.spot.MsgCreatePool
    * pysdk.msg.spot.MsgExitPool
    * pysdk.msg.spot.MsgJoinPool
    * pysdk.msg.spot.MsgSwapAssets
    * pysdk.msg.staking.MsgDelegate
    * pysdk.msg.staking.MsgUndelegate
    * pysdk.msg.staking.MsgWithdrawDelegatorReward

    ### Methods

    `to_pb(self) ‑> google.protobuf.message.Message`
    :   Generate the protobuf message

        Returns:
            Any: The protobuff mesage

`TxBroadcastMode(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   The TxType allows you to choose what type of synchronization you want to
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

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `ASYNC`
    :

    `BLOCK`
    :

    `SYNC`
    :

`TxConfig(gas_wanted: int = 0, gas_multiplier: float = 1.25, gas_price: float = 0.25, broadcast_mode: pysdk.pytypes.common.TxBroadcastMode = TxBroadcastMode.SYNC)`
:   The TxConfig object allows to customize the behavior of the Sdk interface
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

    ### Class variables

    `broadcast_mode: pysdk.pytypes.common.TxBroadcastMode`
    :

    `gas_multiplier: float`
    :

    `gas_price: float`
    :

    `gas_wanted: int`
    :
