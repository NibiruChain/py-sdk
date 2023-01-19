import dataclasses
from typing import List, Union

import nibiru_proto.betterproto.nibiru.dex.v1 as pool_proto

from nibiru.pytypes import Coin, PoolAsset, PoolType, PythonMsg


class MsgsDex:
    """MsgsDex has methods for building messages for transactions on Nibi-Swap.

    Methods:
    - create_pool: Create a pool using the assets specified
    - exit_pool: Exit a pool using the specified pool shares
    - join_pool: Join a pool using the specified tokens
    - swap: Swap the assets provided for the denom specified
    """

    @staticmethod
    def create_pool(
        creator: str,
        swap_fee: float,
        exit_fee: float,
        a: int,
        pool_type: PoolType,
        assets: List[PoolAsset],
    ) -> 'MsgCreatePool':
        return MsgCreatePool(
            creator=creator,
            swap_fee=swap_fee,
            exit_fee=exit_fee,
            a=a,
            pool_type=pool_type,
            assets=assets,
        )

    @staticmethod
    def join_pool(
        sender: str,
        pool_id: int,
        tokens: Union[Coin, List[Coin]],
    ) -> 'MsgJoinPool':
        return MsgJoinPool(sender=sender, pool_id=pool_id, tokens=tokens)

    @staticmethod
    def exit_pool(
        sender: str,
        pool_id: int,
        pool_shares: Coin,
    ) -> 'MsgExitPool':
        return MsgExitPool(sender=sender, pool_id=pool_id, pool_shares=pool_shares)

    @staticmethod
    def swap(
        sender: str,
        pool_id: int,
        token_in: Coin,
        token_out_denom: str,
    ) -> 'MsgSwapAssets':
        return MsgSwapAssets(
            sender=sender,
            pool_id=pool_id,
            token_in=token_in,
            token_out_denom=token_out_denom,
        )


@dataclasses.dataclass
class MsgCreatePool(PythonMsg):
    """
    Create a pool using the assets specified

    Attributes:
        creator (str): The creator address
        swap_fee (float): The swap fee required for the pool
        exit_fee (float): The exit fee required for the pool
        assets (List[PoolAsset]): The assets to compose the pool
    """

    creator: str
    swap_fee: float
    exit_fee: float
    a: int
    pool_type: PoolType
    assets: List[PoolAsset]

    def to_pb(self) -> pool_proto.MsgCreatePool:
        """
        Returns the Message as protobuf object.

        Returns:
            pool_proto.MsgCreatePool: The proto object.

        """
        pool_assets = [
            pool_proto.PoolAsset(
                token=a.token._generate_proto_object(), weight=str(int(a.weight * 1e6))
            )
            for a in self.assets
        ]

        swap_fee_dec = str(int(self.swap_fee * 1e18))
        exit_fee_dec = str(int(self.exit_fee * 1e18))

        return pool_proto.MsgCreatePool(
            creator=self.creator,
            pool_params=pool_proto.PoolParams(
                swap_fee=swap_fee_dec,
                exit_fee=exit_fee_dec,
                pool_type=self.pool_type,
                A=str(int(self.a)),
            ),
            pool_assets=pool_assets,
        )


@dataclasses.dataclass
class MsgJoinPool(PythonMsg):
    """
    Join a pool using the specified tokens

    Attributes:
        sender (str): The creator address
        pool_id (int): The id of the pool to join
        tokens (List[Coin]): The tokens to be bonded in the pool
    """

    sender: str
    pool_id: int
    tokens: Union[Coin, List[Coin]]

    def to_pb(self) -> pool_proto.MsgJoinPool:
        """
        Returns the Message as protobuf object.

        Returns:
            pool_proto.MsgJoinPool: The proto object.

        """
        if isinstance(self.tokens, Coin):
            self.tokens = [self.tokens]
        return pool_proto.MsgJoinPool(
            sender=self.sender,
            pool_id=self.pool_id,
            tokens_in=[token._generate_proto_object() for token in self.tokens],
        )


@dataclasses.dataclass
class MsgExitPool(PythonMsg):
    """
    Exit a pool using the specified pool shares

    Attributes:
        sender (str): The creator address
        pool_id (int): The id of the pool
        pool_shares (Coin): The tokens as share of the pool to exit with
    """

    sender: str
    pool_id: int
    pool_shares: Coin

    def to_pb(self) -> pool_proto.MsgExitPool:
        """
        Returns the Message as protobuf object.

        Returns:
            pool_proto.MsgExitPool: The proto object.

        """
        return pool_proto.MsgExitPool(
            sender=self.sender,
            pool_id=self.pool_id,
            pool_shares=self.pool_shares._generate_proto_object(),
        )


@dataclasses.dataclass
class MsgSwapAssets(PythonMsg):
    """
    Swap the assets provided for the denom specified

    Attributes:
        sender (str): The creator address
        pool_id (int): The id of the pool
        token_in (Coin): The token in we wish to swap with
        token_out_denom (str): The token we expect out of the pool
    """

    sender: str
    pool_id: int
    token_in: Coin
    token_out_denom: str

    def to_pb(self) -> pool_proto.MsgSwapAssets:
        """
        Returns the Message as protobuf object.

        Returns:
            pool_proto.MsgSwapAssets: The proto object.

        """
        return pool_proto.MsgSwapAssets(
            sender=self.sender,
            pool_id=self.pool_id,
            token_in=self.token_in._generate_proto_object(),
            token_out_denom=self.token_out_denom,
        )


class dex:
    """
    The dex class allows to create transactions for the decentralized spot exchange using the queries.
    """

    create_pool: MsgCreatePool
    join_pool: MsgJoinPool
    exit_pool: MsgExitPool
    swap_assets: MsgSwapAssets
