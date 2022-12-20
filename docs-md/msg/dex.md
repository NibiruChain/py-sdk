Module nibiru.msg.dex
=====================

Classes
-------

`MsgCreatePool(creator: str, swap_fee: float, exit_fee: float, a: int, pool_type: <google.protobuf.internal.enum_type_wrapper.EnumTypeWrapper object at 0x7f9fb40d6390>, assets: List[nibiru.pytypes.common.PoolAsset])`
:   Create a pool using the assets specified

    Attributes:
        creator (str): The creator address
        swap_fee (float): The swap fee required for the pool
        exit_fee (float): The exit fee required for the pool
        assets (List[PoolAsset]): The assets to compose the pool

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `a: int`
    :

    `assets: List[nibiru.pytypes.common.PoolAsset]`
    :

    `creator: str`
    :

    `exit_fee: float`
    :

    `pool_type: <google.protobuf.internal.enum_type_wrapper.EnumTypeWrapper object at 0x7f9fb40d6390>`
    :

    `swap_fee: float`
    :

`MsgExitPool(sender: str, pool_id: int, pool_shares: nibiru.pytypes.common.Coin)`
:   Exit a pool using the specified pool shares

    Attributes:
        sender (str): The creator address
        pool_id (int): The id of the pool
        pool_shares (Coin): The tokens as share of the pool to exit with

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `pool_id: int`
    :

    `pool_shares: nibiru.pytypes.common.Coin`
    :

    `sender: str`
    :

`MsgJoinPool(sender: str, pool_id: int, tokens: Union[nibiru.pytypes.common.Coin, List[nibiru.pytypes.common.Coin]])`
:   Join a pool using the specified tokens

    Attributes:
        sender (str): The creator address
        pool_id (int): The id of the pool to join
        tokens (List[Coin]): The tokens to be bonded in the pool

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `pool_id: int`
    :

    `sender: str`
    :

    `tokens: Union[nibiru.pytypes.common.Coin, List[nibiru.pytypes.common.Coin]]`
    :

`MsgSwapAssets(sender: str, pool_id: int, token_in: nibiru.pytypes.common.Coin, token_out_denom: str)`
:   Swap the assets provided for the denom specified

    Attributes:
        sender (str): The creator address
        pool_id (int): The id of the pool
        token_in (Coin): The token in we wish to swap with
        token_out_denom (str): The token we expect out of the pool

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `pool_id: int`
    :

    `sender: str`
    :

    `token_in: nibiru.pytypes.common.Coin`
    :

    `token_out_denom: str`
    :

`MsgsDex()`
:   MsgsDex has methods for building messages for transactions on Nibi-Swap.

    Methods:
    - create_pool: Create a pool using the assets specified
    - exit_pool: Exit a pool using the specified pool shares
    - join_pool: Join a pool using the specified tokens
    - swap: Swap the assets provided for the denom specified

    ### Methods

    `create_pool(creator: str, swap_fee: float, exit_fee: float, a: int, pool_type: <google.protobuf.internal.enum_type_wrapper.EnumTypeWrapper object at 0x7f9fb40d6390>, assets: List[nibiru.pytypes.common.PoolAsset]) ‑> nibiru.msg.dex.MsgCreatePool`
    :

    `exit_pool(sender: str, pool_id: int, pool_shares: nibiru.pytypes.common.Coin) ‑> nibiru.msg.dex.MsgExitPool`
    :

    `join_pool(sender: str, pool_id: int, tokens: Union[nibiru.pytypes.common.Coin, List[nibiru.pytypes.common.Coin]]) ‑> nibiru.msg.dex.MsgJoinPool`
    :

    `swap(sender: str, pool_id: int, token_in: nibiru.pytypes.common.Coin, token_out_denom: str) ‑> nibiru.msg.dex.MsgSwapAssets`
    :

`dex()`
:   The dex class allows to create transactions for the decentralized spot exchange using the queries.

    ### Class variables

    `create_pool: nibiru.msg.dex.MsgCreatePool`
    :

    `exit_pool: nibiru.msg.dex.MsgExitPool`
    :

    `join_pool: nibiru.msg.dex.MsgJoinPool`
    :

    `swap_assets: nibiru.msg.dex.MsgSwapAssets`
    :
