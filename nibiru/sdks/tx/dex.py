from typing import List

from nibiru.common import PoolAsset, Coin
from nibiru.proto.dex.v1 import pool_pb2 as pool_tx_pb
from nibiru.proto.dex.v1 import tx_pb2 as dex_tx_pb
from nibiru.utils import to_sdk_dec
from nibiru.proto.cosmos.base.abci.v1beta1 import abci_pb2 as abci_type

from .common import Tx


class Dex(Tx):
    def create_pool(
        self,
        creator: str,
        swap_fee: float,
        exit_fee: float,
        assets: List[PoolAsset],
        **kwargs
    ) -> abci_type.TxResponse:
        """
        Create a pool using the assets specified

        Args:
            creator (str): The creator address
            swap_fee (float): The swap fee required for the pool
            exit_fee (float): The exit fee required for the pool
            assets (List[PoolAsset]): The assets to compose the pool

        Returns:
            abci_type.TxResponse: The output of the transaction
        """
        pool_assets = [
            pool_tx_pb.PoolAsset(
                token=a.token._generate_proto_object(), weight=str(int(a.weight*1e6))
            ) for a in assets
        ]

        swap_fee_dec = str(int(swap_fee * 1e18))
        exit_fee_dec = str(int(exit_fee * 1e18))

        msg= dex_tx_pb.MsgCreatePool(
            creator=creator,
            pool_params=pool_tx_pb.PoolParams(swap_fee=swap_fee_dec, exit_fee=exit_fee_dec),
            pool_assets=pool_assets,
        )
        return super().execute_msg(msg, **kwargs)

    def join_pool(self, sender: str, pool_id: int, tokens: List[Coin], **kwargs)->abci_type.TxResponse:
        """
        Join a pool using the specified tokens

        Args:
            sender (str): The creator address
            pool_id (int): The id of the pool to join
            tokens (List[Coin]): The tokens to be bonded in the pool

        Returns:
            abci_type.TxResponse: The output of the transaction
        """
        msg = dex_tx_pb.MsgJoinPool(
            sender=sender,
            pool_id=pool_id,
            tokens_in=[token._generate_proto_object() for token in tokens],
        )
        return super().execute_msg(msg, **kwargs)

    def exit_pool(self, sender: str, pool_id: int, pool_shares: Coin, **kwargs)->abci_type.TxResponse:
        """
        Exit a pool using the specified pool shares

        Args:
            sender (str): The creator address
            pool_id (int): The id of the pool
            pool_shares (Coin): The tokens as share of the pool to exit with

        Returns:
            abci_type.TxResponse: The output of the transaction
        """
        msg = dex_tx_pb.MsgExitPool(
            sender=sender,
            pool_id=pool_id,
            pool_shares=pool_shares._generate_proto_object(),
        )
        return super().execute_msg(msg, **kwargs)

    def swap_assets(self, sender: str, pool_id: int, token_in: Coin, token_out_denom, **kwargs)->abci_type.TxResponse:
        """
        Swap the assets provided for the denom specified

        Args:
            sender (str): The creator address
            pool_id (int): The id of the pool
            token_in (Coin): The token in we wish to swap with
            token_out_denom (_type_): The token we expect out of the pool

        Returns:
            abci_type.TxResponse: The output of the transaction
        """
        msg = dex_tx_pb.MsgSwapAssets(
            sender=sender,
            pool_id=pool_id,
            token_in=token_in._generate_proto_object(),
            token_out_denom=token_out_denom,
        )

        return super().execute_msg(msg, **kwargs)
