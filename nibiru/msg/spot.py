import dataclasses
from typing import List, Union

from nibiru_proto.proto.spot.v1 import pool_pb2 as pool_tx_pb
from nibiru_proto.proto.spot.v1 import tx_pb2 as pb

from nibiru.pytypes import Coin, PoolAsset, PoolType, PythonMsg


class MsgsSpot:
    """MsgsSpot has methods for building messages for transactions on Nibi-Swap.

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

    def to_pb(self) -> pb.MsgCreatePool:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgCreatePool: The proto object.

        """
        pool_assets = [
            pool_tx_pb.PoolAsset(
                token=a.token._generate_proto_object(), weight=str(int(a.weight * 1e6))
            )
            for a in self.assets
        ]

        swap_fee_dec = str(int(self.swap_fee * 1e18))
        exit_fee_dec = str(int(self.exit_fee * 1e18))

        return pb.MsgCreatePool(
            creator=self.creator,
            pool_params=pool_tx_pb.PoolParams(
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

    def to_pb(self) -> pb.MsgJoinPool:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgJoinPool: The proto object.

        """
        if isinstance(self.tokens, Coin):
            self.tokens = [self.tokens]
        return pb.MsgJoinPool(
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

    def to_pb(self) -> pb.MsgExitPool:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgExitPool: The proto object.

        """
        return pb.MsgExitPool(
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

    def to_pb(self) -> pb.MsgSwapAssets:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgSwapAssets: The proto object.

        """
        return pb.MsgSwapAssets(
            sender=self.sender,
            pool_id=self.pool_id,
            token_in=self.token_in._generate_proto_object(),
            token_out_denom=self.token_out_denom,
        )


class spot:
    """
    The spot class allows to create transactions for the decentralized spot exchange using the queries.
    """

    create_pool: MsgCreatePool
    join_pool: MsgJoinPool
    exit_pool: MsgExitPool
    swap_assets: MsgSwapAssets
