# perp_test.py

from typing import Dict, List

import pytest

import nibiru
import nibiru.msg
import tests
from nibiru import Coin, PoolAsset
from nibiru.exceptions import SimulationError
from nibiru.pytypes import PoolType
from tests import transaction_must_succeed

PRECISION = 6


@pytest.mark.order(1)
def test_dex_create_pool(sdk_val: nibiru.Sdk):
    """
    Test the workflow for pools
    """

    err_same_denom: str = "a pool with the same denoms already exists"
    err_insufficient_funds: str = "smaller than 1000000000unibi: insufficient funds"

    def has_reasonable_err(err) -> bool:
        has_err_same_denom = err_same_denom in str(err)
        has_err_insufficient_funds = err_insufficient_funds in str(err)
        return has_err_same_denom or has_err_insufficient_funds

    try:
        tx_output = sdk_val.tx.execute_msgs(
            nibiru.msg.MsgCreatePool(
                creator=sdk_val.address,
                swap_fee=0.01,
                exit_fee=0.02,
                assets=[
                    PoolAsset(token=Coin(100, "unibi"), weight=50),
                    PoolAsset(token=Coin(1000, "unusd"), weight=50),
                ],
                pool_type=PoolType.BALANCER,
                a=0,
            )
        )

        transaction_must_succeed(tx_output)
    except SimulationError as simulation_error:
        assert has_reasonable_err(simulation_error), simulation_error

    """
    # # TODO fix: need usdc on-chain  to do this
    try:
        tx_output = sdk_val.tx.execute_msgs(
            nibiru.msg.MsgCreatePool(
                creator=sdk_val.address,
                swap_fee=0.01,
                exit_fee=0.02,
                assets=[
                    PoolAsset(token=Coin(1000, "unusd"), weight=50),
                    PoolAsset(token=Coin(100, "uusdc"), weight=50),
                ],
                pool_type=PoolType.STABLESWAP,
                a=10,
            )
        )
        transaction_must_succeed(tx_output)
    except SimulationError as simulation_error:
        assert has_reasonable_err(simulation_error), simulation_error
    """


@pytest.fixture
def pools(sdk_val: nibiru.Sdk) -> List[dict]:
    return sdk_val.query.dex.pools()


@pytest.fixture
def pool_ids(pools: List[dict]) -> Dict[str, int]:
    pool_ids: Dict[str, int] = {}
    # for pool_assets in ["unibi:unusd", "unusd:uusdc"]:
    # # TODO fix: need usdc on-chain  to do this
    for pool_assets in ["unibi:unusd"]:
        pool_assets_expected = set(pool_assets.split(":"))

        any(
            [
                pool_assets_expected
                == set(
                    [
                        pool["poolAssets"][0]["token"]["denom"],
                        pool["poolAssets"][1]["token"]["denom"],
                    ]
                )
                for pool in pools
            ]
        )

        pool_id = int(
            [
                pool["id"]
                for pool in pools
                if pool_assets_expected
                == set(
                    [
                        pool["poolAssets"][0]["token"]["denom"],
                        pool["poolAssets"][1]["token"]["denom"],
                    ]
                )
            ][0]
        )
        pool_ids[pool_assets] = pool_id
    return pool_ids


@pytest.mark.order(2)
def test_dex_query_pools(pools: List[dict]):
    """TODO test something about the shape of the pools response"""


@pytest.mark.order(3)
def test_dex_join_pool(sdk_val: nibiru.Sdk, pool_ids: Dict[str, int]):
    tx_output = sdk_val.tx.execute_msgs(
        [
            nibiru.msg.MsgJoinPool(
                sender=sdk_val.address,
                pool_id=pool_ids["unibi:unusd"],
                tokens=[Coin(1000, "unibi"), Coin(100, "unusd")],
            ),
        ]
    )
    transaction_must_succeed(tx_output)


@pytest.mark.order(4)
def test_dex_swap(sdk_val: nibiru.Sdk, pool_ids: Dict[str, int]):
    tx_output = sdk_val.tx.execute_msgs(
        [
            # # TODO fix: need usdc on-chain  to do this
            # nibiru.msg.MsgJoinPool(
            #     sender=sdk_agent.address,
            #     pool_id=pool_ids["unusd:uusdc"],
            #     tokens=[Coin(100, "uusdc"), Coin(100, "unusd")],
            # ),
            # # TODO fix: need usdc on-chain  to do this
            # nibiru.msg.MsgSwapAssets(
            #     sender=sdk_agent.address,
            #     pool_id=pool_ids["unusd:uusdc"],
            #     token_in=Coin(100, "uusdc"),
            #     token_out_denom="unusd",
            # ),
            nibiru.msg.MsgSwapAssets(
                sender=sdk_val.address,
                pool_id=pool_ids["unibi:unusd"],
                token_in=Coin(100, "unusd"),
                token_out_denom="unibi",
            ),
        ]
    )
    transaction_must_succeed(tx_output)


@pytest.mark.order(5)
def test_dex_exit_pool(sdk_val: nibiru.Sdk):
    balance = sdk_val.query.get_bank_balances(sdk_val.address)["balances"]

    pool_tokens: List[str] = [
        pool_token for pool_token in balance if "nibiru/pool" in pool_token
    ]
    if pool_tokens:
        tx_output = sdk_val.tx.execute_msgs(
            [
                nibiru.msg.MsgExitPool(
                    sender=sdk_val.address,
                    pool_id=int(pool_token["denom"].split("/")[-1]),
                    pool_shares=Coin(pool_token["amount"], pool_token["denom"]),
                )
                for pool_token in pool_tokens
            ]
        )
        transaction_must_succeed(tx_output)
    else:
        tests.LOGGER.info(
            "skipped test for 'nibid tx dex exit-pool' because\n"
            + f"{sdk_val.address} did not have LP shares"
        )
