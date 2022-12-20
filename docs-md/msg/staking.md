Module nibiru.msg.staking
=========================

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
        delegator_address (str)
        validator_address (str)

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `delegator_address: str`
    :

    `validator_address: str`
    :

`MsgsStaking()`
:   Messages for the x/staking and x/distribution modules.

    Methods:
    - delegate: Delegate tokens to a validator
    - undelegate: Undelegate tokens from a validator
    - withdraw_delegator_reward: Withdraw the reward from a validator

    ### Methods

    `delegate(delegator_address: str, validator_address: str, amount: float) ‑> nibiru.msg.staking.MsgDelegate`
    :   Delegate tokens to a validator

        Attributes:
            delegator_address: str
            validator_address: str
            amount: float

        Returns:
            MsgDelegate: PythonMsg for type 'cosmos.staking.v1beta1.MsgDelegate'

    `undelegate(delegator_address: str, validator_address: str, amount: float) ‑> nibiru.msg.staking.MsgUndelegate`
    :   Undelegate tokens from a validator

        Attributes:
            delegator_address (str): Bech32 address for the delegator
            validator_address (str): Bech32 valoper address
            amount (float): Amount of unibi to undelegate.

    `withdraw_delegator_reward(delegator_address: str, validator_address: str) ‑> nibiru.msg.staking.MsgWithdrawDelegatorReward`
    :   TODO
        Withdraw the reward from a validator

        Attributes:
            delegator_address (str)
            validator_address (str)

        Returns:
            MsgWithdrawDelegatorReward: _description_
