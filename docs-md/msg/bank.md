Module nibiru.msg.bank
======================

Classes
-------

`MsgSend(from_address: str, to_address: str, coins: Union[nibiru.pytypes.common.Coin, List[nibiru.pytypes.common.Coin]])`
:   Send tokens from one account to another. PythonMsg corresponding to the
    'cosmos.bank.v1beta1.MsgSend' message.

    Attributes:
        from_address (str): The address of the sender
        to_address (str): The address of the receiver
        coins (List[Coin]): The list of coins to send

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `coins: Union[nibiru.pytypes.common.Coin, List[nibiru.pytypes.common.Coin]]`
    :

    `from_address: str`
    :

    `to_address: str`
    :

`MsgsBank()`
:   Messages for the x/bank module.

    Methods:
    - send: Send tokens from one account to another

    ### Methods

    `send(from_address: str, to_address: str, coins: Union[nibiru.pytypes.common.Coin, List[nibiru.pytypes.common.Coin]]) ‑> nibiru.msg.bank.MsgSend`
    :   Send tokens from one account to another

        Attributes:
            from_address (str): The address of the sender
            to_address (str): The address of the receiver
            coins (List[Coin]): The list of coins to send

        Returns:
            MsgSend: PythonMsg corresponding to the 'cosmos.bank.v1beta1.MsgSend' message
