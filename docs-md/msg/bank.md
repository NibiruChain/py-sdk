Module nibiru.msg.bank
======================

Classes
-------

`MsgDelegate(delegator_address: str, validator_address: str, amount: float)`
:   Delegate tokens to a validator

    Attributes:
        delegator_address: str
        validator_address: str
        amount: float

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `amount: float`
    :

    `delegator_address: str`
    :

    `validator_address: str`
    :

`MsgSend(from_address: str, to_address: str, coins: Union[nibiru.pytypes.common.Coin, List[nibiru.pytypes.common.Coin]])`
:   Send tokens from one account to another

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

`MsgUndelegate(delegator_address: str, validator_address: str, amount: float)`
:   Undelegate tokens from a validator

    Attributes:
        delegator_address: str
        validator_address: str
        amount: float

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `amount: float`
    :

    `delegator_address: str`
    :

    `validator_address: str`
    :

`MsgWithdrawDelegatorReward(delegator_address: str, validator_address: str)`
:   Withdraw the reward from a validator

    Attributes:
        delegator_address: str
        validator_address: str

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `delegator_address: str`
    :

    `validator_address: str`
    :
