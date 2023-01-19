Module nibiru.msg.msg
=====================

Classes
-------

`MsgClient()`
:   The 'MsgClient' exposes all available messages in the Nibiru Chain Python SDK.
    The class attributes of the client separate these messages by module.

    Attributes:
        bank: Methods for the Cosmos x/bank module.
        dex: Methods for the Nibiru Chain x/dex module.
        perp: Methods for the Nibiru Chain x/perp module
        staking: Methods for the Cosmos x/staking and x/distribution modules.

    ### Class variables

    `bank`
    :   Messages for the x/bank module.

        Methods:
        - send: Send tokens from one account to another

    `dex`
    :   MsgsDex has methods for building messages for transactions on Nibi-Swap.

        Methods:
        - create_pool: Create a pool using the assets specified
        - exit_pool: Exit a pool using the specified pool shares
        - join_pool: Join a pool using the specified tokens
        - swap: Swap the assets provided for the denom specified

    `perp`
    :   Messages for the Nibiru Chain x/perp module

        Methods:
        - open_position
        - close_position:
        - add_margin: Deleverages a position by adding margin to back it.
        - remove_margin: Increases the leverage of the position by removing margin.

    `staking`
    :   Messages for the x/staking and x/distribution modules.

        Methods:
        - delegate: Delegate tokens to a validator
        - undelegate: Undelegate tokens from a validator
        - withdraw_delegator_reward: Withdraw the reward from a validator
