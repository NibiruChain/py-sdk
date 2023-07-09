# perp_test.py

from typing import Dict, List, Literal, Union, cast

import pytest

import nibiru
import tests
from nibiru import Coin, PoolAsset, utils
from nibiru.exceptions import SimulationError
from nibiru.pytypes import PoolType

PRECISION = 6


class SpotErrors:
    same_denom = "a pool with the same denoms already exists"
    insufficient_funds = "smaller than 1000000000unibi: insufficient funds"
    swap_low_unusd_in_pool = "tokenIn (unusd) must be higher to perform a swap"
    no_pool_shares = "0nibiru/pool/"


def test_spot_create_pool(sdk_val: nibiru.Sdk):
    """
    Test the workflow for pools
    """

    try:
        tx_output = sdk_val.tx.execute_msgs(
            nibiru.Msg.spot.create_pool(
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

        tests.broadcast_tx_must_succeed(tx_output)
    except SimulationError as simulation_error:
        tests.raises(
            [SpotErrors.same_denom, SpotErrors.insufficient_funds], simulation_error
        )

    """
    # # TODO fix: need usdc on-chain  to do this
    try:
        tx_output = sdk_val.tx.execute_msgs(
            nibiru.Msg.spot.create_pool(
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
        tests.raw_sync_tx_must_succeed(tx_output)
    except SimulationError as simulation_error:
        assert has_reasonable_err(simulation_error), simulation_error
    """


@pytest.mark.order(after="test_spot_create_pool")
@pytest.fixture
def pools(sdk_val: nibiru.Sdk) -> List[dict]:
    pools_resp = sdk_val.query.spot.pools()
    if pools_resp:
        return sdk_val.query.spot.pools()
    else:
        return []


@pytest.mark.order(after="pools")
@pytest.fixture
def pool_ids(pools: List[dict]) -> Dict[str, int]:
    pool_ids: Dict[str, int] = {}
    if not pools:
        return pool_ids
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


@pytest.mark.order(after="test_spot_create_pool")
def test_spot_query_pools(pools: List[dict]):
    if not pools:
        return

    pool = pools[0]
    keys = ["id", "address", "poolParams", "poolAssets", "totalWeight", "totalShares"]
    assert isinstance(pool, dict)
    utils.dict_keys_must_match(pool, keys)


@pytest.mark.order(after="test_spot_query_pools")
def test_spot_join_pool(sdk_val: nibiru.Sdk, pool_ids: Dict[str, int]):
    if not pool_ids:
        return
    try:
        tx_output = sdk_val.tx.execute_msgs(
            [
                nibiru.Msg.spot.join_pool(
                    sender=sdk_val.address,
                    pool_id=pool_ids["unibi:unusd"],
                    tokens=[Coin(1000, "unibi"), Coin(100, "unusd")],
                ),
            ]
        )
        tests.broadcast_tx_must_succeed(tx_output)
    except BaseException as err:
        tests.raises(SpotErrors.no_pool_shares, err)


@pytest.mark.order(after="test_spot_join_pool")
def test_spot_swap(sdk_val: nibiru.Sdk, pool_ids: Dict[str, int]):
    if not pool_ids:
        return
    try:
        tx_output = sdk_val.tx.execute_msgs(
            [
                # # TODO fix: need usdc on-chain  to do this
                # nibiru.Msg.spot.join_pool(
                #     sender=sdk_agent.address,
                #     pool_id=pool_ids["unusd:uusdc"],
                #     tokens=[Coin(100, "uusdc"), Coin(100, "unusd")],
                # ),
                # # TODO fix: need usdc on-chain  to do this
                # nibiru.Msg.spot.swap(
                #     sender=sdk_agent.address,
                #     pool_id=pool_ids["unusd:uusdc"],
                #     token_in=Coin(100, "uusdc"),
                #     token_out_denom="unusd",
                # ),
                nibiru.Msg.spot.swap(
                    sender=sdk_val.address,
                    pool_id=pool_ids["unibi:unusd"],
                    token_in=Coin(100, "unusd"),
                    token_out_denom="unibi",
                ),
            ]
        )
        tests.broadcast_tx_must_succeed(tx_output)
    except BaseException as err:
        tests.raises(SpotErrors.swap_low_unusd_in_pool, err)


@pytest.mark.order(after="test_spot_swap")
def test_spot_exit_pool(sdk_val: nibiru.Sdk):
    all_balance_maps = sdk_val.query.get_bank_balances(sdk_val.address)["balances"]

    balance_maps: List[Dict[Literal["denom", "amount"], Union[str, int]]] = [
        balance_map
        for balance_map in all_balance_maps
        if "nibiru/pool" in cast(str, balance_map["denom"])
    ]
    msgs = []
    for pool_token in balance_maps:
        denom = pool_token.get("denom")
        assert isinstance(denom, str)

        pool_id = denom.split("/")[-1]
        assert isinstance(pool_id, str)

        amount = pool_token.get("amount")
        assert isinstance(amount, (str, int))
        msgs.append(
            nibiru.Msg.spot.exit_pool(
                sender=sdk_val.address,
                pool_id=int(pool_id),
                pool_shares=Coin(int(amount), denom),
            )
        )
    if balance_maps:
        broadcast_resp = sdk_val.tx.execute_msgs(msgs=msgs)
        tests.broadcast_tx_must_succeed(res=broadcast_resp)
    if not balance_maps:
        tests.LOGGER.info(
            "skipped test for 'nibid tx spot exit-pool' because\n"
            + f"{sdk_val.address} did not have LP shares"
        )
