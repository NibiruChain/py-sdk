Module pysdk.msg.spot
=====================

Classes
-------

`MsgCreatePool(creator: str, swap_fee: float, exit_fee: float, a: int, pool_type: <google.protobuf.internal.enum_type_wrapper.EnumTypeWrapper object at 0x7f49922c6dc0>, assets: List[pysdk.pytypes.common.PoolAsset])`
:   Create a pool using the assets specified

    Attributes:
        creator (str): The creator address
        swap_fee (float): The swap fee required for the pool
        exit_fee (float): The exit fee required for the pool
        assets (List[PoolAsset]): The assets to compose the pool

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `a: int`
    :

    `assets: List[pysdk.pytypes.common.PoolAsset]`
    :

    `creator: str`
    :

    `exit_fee: float`
    :

    `pool_type: <google.protobuf.internal.enum_type_wrapper.EnumTypeWrapper object at 0x7f49922c6dc0>`
    :

    `swap_fee: float`
    :

    ### Methods

    `to_pb(self) ‑> nibiru.spot.v1.tx_pb2.MsgCreatePool`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgCreatePool: The proto object.

`MsgExitPool(sender: str, pool_id: int, pool_shares: pysdk.pytypes.common.Coin)`
:   Exit a pool using the specified pool shares

    Attributes:
        sender (str): The creator address
        pool_id (int): The id of the pool
        pool_shares (Coin): The tokens as share of the pool to exit with

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `pool_id: int`
    :

    `pool_shares: pysdk.pytypes.common.Coin`
    :

    `sender: str`
    :

    ### Methods

    `to_pb(self) ‑> nibiru.spot.v1.tx_pb2.MsgExitPool`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgExitPool: The proto object.

`MsgJoinPool(sender: str, pool_id: int, tokens: Union[pysdk.pytypes.common.Coin, List[pysdk.pytypes.common.Coin]])`
:   Join a pool using the specified tokens

    Attributes:
        sender (str): The creator address
        pool_id (int): The id of the pool to join
        tokens (List[Coin]): The tokens to be bonded in the pool

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `pool_id: int`
    :

    `sender: str`
    :

    `tokens: Union[pysdk.pytypes.common.Coin, List[pysdk.pytypes.common.Coin]]`
    :

    ### Methods

    `to_pb(self) ‑> nibiru.spot.v1.tx_pb2.MsgJoinPool`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgJoinPool: The proto object.

`MsgSwapAssets(sender: str, pool_id: int, token_in: pysdk.pytypes.common.Coin, token_out_denom: str)`
:   Swap the assets provided for the denom specified

    Attributes:
        sender (str): The creator address
        pool_id (int): The id of the pool
        token_in (Coin): The token in we wish to swap with
        token_out_denom (str): The token we expect out of the pool

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `pool_id: int`
    :

    `sender: str`
    :

    `token_in: pysdk.pytypes.common.Coin`
    :

    `token_out_denom: str`
    :

    ### Methods

    `to_pb(self) ‑> nibiru.spot.v1.tx_pb2.MsgSwapAssets`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgSwapAssets: The proto object.

`MsgsSpot()`
:   MsgsSpot has methods for building messages for transactions on Nibi-Swap.

    Methods:
    - create_pool: Create a pool using the assets specified
    - exit_pool: Exit a pool using the specified pool shares
    - join_pool: Join a pool using the specified tokens
    - swap: Swap the assets provided for the denom specified

    ### Static methods

    `create_pool(creator: str, swap_fee: float, exit_fee: float, a: int, pool_type: <google.protobuf.internal.enum_type_wrapper.EnumTypeWrapper object at 0x7f49922c6dc0>, assets: List[pysdk.pytypes.common.PoolAsset]) ‑> pysdk.msg.spot.MsgCreatePool`
    :

    `exit_pool(sender: str, pool_id: int, pool_shares: pysdk.pytypes.common.Coin) ‑> pysdk.msg.spot.MsgExitPool`
    :

    `join_pool(sender: str, pool_id: int, tokens: Union[pysdk.pytypes.common.Coin, List[pysdk.pytypes.common.Coin]]) ‑> pysdk.msg.spot.MsgJoinPool`
    :

    `swap(sender: str, pool_id: int, token_in: pysdk.pytypes.common.Coin, token_out_denom: str) ‑> pysdk.msg.spot.MsgSwapAssets`
    :

`spot()`
:   The spot class allows to create transactions for the decentralized spot exchange using the queries.

    ### Class variables

    `create_pool: pysdk.msg.spot.MsgCreatePool`
    :

    `exit_pool: pysdk.msg.spot.MsgExitPool`
    :

    `join_pool: pysdk.msg.spot.MsgJoinPool`
    :

    `swap_assets: pysdk.msg.spot.MsgSwapAssets`
    :
