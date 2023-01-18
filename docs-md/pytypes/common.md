Module nibiru.pytypes.common
============================

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

    `ADD`
    :

    `REMOVE`
    :

`PoolAsset(token: nibiru.pytypes.common.Coin, weight: float)`
:   PoolAsset(token: nibiru.pytypes.common.Coin, weight: float)

    ### Class variables

    `token: nibiru.pytypes.common.Coin`
    :

    `weight: float`
    :

`PythonMsg()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * nibiru.msg.bank.MsgSend
    * nibiru.msg.dex.MsgCreatePool
    * nibiru.msg.dex.MsgExitPool
    * nibiru.msg.dex.MsgJoinPool
    * nibiru.msg.dex.MsgSwapAssets
    * nibiru.msg.perp.MsgAddMargin
    * nibiru.msg.perp.MsgClosePosition
    * nibiru.msg.perp.MsgLiquidate
    * nibiru.msg.perp.MsgOpenPosition
    * nibiru.msg.perp.MsgRemoveMargin
    * nibiru.msg.staking.MsgDelegate
    * nibiru.msg.staking.MsgUndelegate
    * nibiru.msg.staking.MsgWithdrawDelegatorReward

    ### Methods

    `to_pb(self) ‑> google.protobuf.message.Message`
    :   Generate the protobuf message

        Returns:
            Any: The protobuff mesage

`Side(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `BUY`
    :

    `SELL`
    :

`TxConfig(gas_wanted: int = 0, gas_multiplier: float = 1.25, gas_price: float = 0.25, tx_type: nibiru.pytypes.common.TxType = TxType.BLOCK)`
:   The TxConfig object allows to customize the behavior of the Sdk interface when a transaction is sent.

    Args:
        gas_wanted (int, optional): Set the absolute gas_wanted to be used.
            Defaults to 0.
        gas_multiplier (float, optional): Set the gas multiplier that's being
            applied to the estimated gas. If gas_wanted is set, this property
            is ignored. Defaults to 0.
        gas_price (float, optional): Set the gas price used to calculate the fee.
            Defaults to 0.25.
        tx_type (TxType, optional): Configure how to execute the tx.
            Defaults to TxType.BLOCK.

    ### Class variables

    `gas_multiplier: float`
    :

    `gas_price: float`
    :

    `gas_wanted: int`
    :

    `tx_type: nibiru.pytypes.common.TxType`
    :

`TxType(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   The TxType allows you to choose what type of synchronization you want to use
    to send transaction

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `ASYNC`
    :   The CLI returns immediately (transaction might fail silently).
        If you send a transaction with this option, it is recommended to query the transaction output using the hash of the
        transaction given by the output of the tx call.

    `BLOCK`
    :   The tx function will wait unitl the tx is be committed in a block.
        This have the effect of having the full log of the transaction available with the output of the method. These logs
        will include information as to coin sent and received, states changed etc.

    `SYNC`
    :   The CLI waits for a CheckTx execution response only.
        Each full-node that receives a transaction sends a CheckTx to the application layer to check for validity, and
        receives an abci.ResponseCheckTx. If the Tx passes the checks, it is held in the nodes' Mempool , an in-memory pool
        of transactions unique to each node pending inclusion in a block - honest nodes will discard Tx if it is found to
        be invalid.

        Prior to consensus, nodes continuously check incoming transactions and gossip them to their peers.
