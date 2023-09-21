Module pysdk.msg.bank
=====================

Classes
-------

`MsgSend(from_address: str, to_address: str, coins: Union[pysdk.pytypes.common.Coin, List[pysdk.pytypes.common.Coin]])`
:   Send tokens from one account to another. PythonMsg corresponding to the
    'cosmos.bank.v1beta1.MsgSend' message.

    Attributes:
        from_address (str): The address of the sender
        to_address (str): The address of the receiver
        coins (Union[Coin, List[Coin]]): The list of coins to send

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `coins: Union[pysdk.pytypes.common.Coin, List[pysdk.pytypes.common.Coin]]`
    :

    `from_address: str`
    :

    `to_address: str`
    :

    ### Methods

    `to_pb(self) ‑> cosmos.bank.v1beta1.tx_pb2.MsgSend`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgSend: The proto object.

`MsgsBank()`
:   Messages for the x/bank module.

    Methods:
    - send: Send tokens from one account to another

    ### Static methods

    `send(from_address: str, to_address: str, coins: Union[pysdk.pytypes.common.Coin, List[pysdk.pytypes.common.Coin]]) ‑> pysdk.msg.bank.MsgSend`
    :   Send tokens from one account to another

        Attributes:
            from_address (str): The address of the sender
            to_address (str): The address of the receiver
            coins (List[Coin]): The list of coins to send

        Returns:
            MsgSend: PythonMsg corresponding to the 'cosmos.bank.v1beta1.MsgSend' message
