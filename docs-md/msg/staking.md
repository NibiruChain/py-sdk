Module pysdk.msg.staking
========================

Classes
-------

`MsgDelegate(delegator_address: str, validator_address: str, amount: float)`
:   Delegate tokens to a validator

    Attributes:
        delegator_address: str
        validator_address: str
        amount: float

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `amount: float`
    :

    `delegator_address: str`
    :

    `validator_address: str`
    :

    ### Methods

    `to_pb(self) ‑> cosmos.staking.v1beta1.tx_pb2.MsgDelegate`
    :   Returns the Message as protobuf object.

        Returns:
            staking_pb.MsgDelegate: The proto object.

`MsgUndelegate(delegator_address: str, validator_address: str, amount: float)`
:   Undelegate tokens from a validator

    Attributes:
        delegator_address: str
        validator_address: str
        amount: float

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `amount: float`
    :

    `delegator_address: str`
    :

    `validator_address: str`
    :

    ### Methods

    `to_pb(self) ‑> cosmos.staking.v1beta1.tx_pb2.MsgUndelegate`
    :   Returns the Message as protobuf object.

        Returns:
            staking_pb.MsgUndelegate: The proto object.

`MsgWithdrawDelegatorReward(delegator_address: str, validator_address: str)`
:   Withdraw the reward from a validator

    Attributes:
        delegator_address (str)
        validator_address (str)

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `delegator_address: str`
    :

    `validator_address: str`
    :

    ### Methods

    `to_pb(self) ‑> cosmos.distribution.v1beta1.tx_pb2.MsgWithdrawDelegatorReward`
    :   Returns the Message as protobuf object.

        Returns:
            tx_pb.MsgWithdrawDelegatorReward: The proto object.

`MsgsStaking()`
:   Messages for the x/staking and x/distribution modules.

    Methods:
    - delegate: Delegate tokens to a validator
    - undelegate: Undelegate tokens from a validator
    - withdraw_delegator_reward: Withdraw the reward from a validator

    ### Static methods

    `delegate(delegator_address: str, validator_address: str, amount: float) ‑> pysdk.msg.staking.MsgDelegate`
    :   Delegate tokens to a validator

        Attributes:
            delegator_address: str
            validator_address: str
            amount: float

        Returns:
            MsgDelegate: PythonMsg for type 'cosmos.staking.v1beta1.MsgDelegate'

    `undelegate(delegator_address: str, validator_address: str, amount: float) ‑> pysdk.msg.staking.MsgUndelegate`
    :   Undelegate tokens from a validator

        Attributes:
            delegator_address (str): Bech32 address for the delegator
            validator_address (str): Bech32 valoper address
            amount (float): Amount of unibi to undelegate.

    `withdraw_delegator_reward(delegator_address: str, validator_address: str) ‑> pysdk.msg.staking.MsgWithdrawDelegatorReward`
    :   TODO
        Withdraw the reward from a validator

        Attributes:
            delegator_address (str)
            validator_address (str)

        Returns:
            MsgWithdrawDelegatorReward: _description_
