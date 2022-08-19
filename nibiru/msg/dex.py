import dataclasses
from typing import List

from nibiru_proto.proto.dex.v1 import pool_pb2 as pool_tx_pb
from nibiru_proto.proto.dex.v1 import tx_pb2 as pb

from nibiru.common import Coin, PoolAsset, PythonMsg


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
    assets: List[PoolAsset]

    def to_pb(self) -> pb.MsgCreatePool:
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
                swap_fee=swap_fee_dec, exit_fee=exit_fee_dec
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
    tokens: List[Coin]

    def to_pb(self) -> pb.MsgJoinPool:
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
    pool_shares: List[Coin]

    def to_pb(self) -> pb.MsgExitPool:
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
        return pb.MsgSwapAssets(
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
