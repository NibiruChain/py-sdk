# perp_test.py

from typing import Dict, List, Literal, Union, cast

import pytest

import nibiru
import tests
from nibiru import ChainClient, Coin, PoolAsset, pytypes, utils
from nibiru.exceptions import SimulationError

PRECISION = 6


class SpotErrors:
    same_denom = "a pool with the same denoms already exists"
    insufficient_funds = "smaller than 1000000000unibi: insufficient funds"
    swap_low_unusd_in_pool = "tokenIn (unusd) must be higher to perform a swap"
    no_pool_shares = "0pysdk.pool/"


def test_spot_create_pool(client_validator: ChainClient):
    """
    Test the workflow for pools
    """

    try:
        tx_output = client_validator.tx.execute_msgs(
            nibiru.Msg.spot.create_pool(
                creator=client_validator.address,
                swap_fee=0.01,
                exit_fee=0.02,
                assets=[
                    PoolAsset(token=Coin(100, "unibi"), weight=50),
                    PoolAsset(token=Coin(1000, "unusd"), weight=50),
                ],
                pool_type=pytypes.PoolType.BALANCER,
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
        tx_output = client_validator.tx.execute_msgs(
            pysdk.Msg.spot.create_pool(
                creator=client_validator.address,
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
def pools(client_validator) -> List[dict]:
    pools_resp = client_validator.query.spot.pools()
    if pools_resp:
        return client_validator.query.spot.pools()
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
def test_spot_join_pool(client_validator, pool_ids: Dict[str, int]):
    if not pool_ids:
        return
    try:
        tx_output = client_validator.tx.execute_msgs(
            [
                nibiru.Msg.spot.join_pool(
                    sender=client_validator.address,
                    pool_id=pool_ids["unibi:unusd"],
                    tokens=[Coin(1000, "unibi"), Coin(100, "unusd")],
                ),
            ]
        )
        tests.broadcast_tx_must_succeed(tx_output)
    except BaseException as err:
        tests.raises(SpotErrors.no_pool_shares, err)


@pytest.mark.order(after="test_spot_join_pool")
def test_spot_swap(client_validator, pool_ids: Dict[str, int]):
    if not pool_ids:
        return
    try:
        tx_output = client_validator.tx.execute_msgs(
            [
                # # TODO fix: need usdc on-chain  to do this
                # pysdk.Msg.spot.join_pool(
                #     sender=sdk_agent.address,
                #     pool_id=pool_ids["unusd:uusdc"],
                #     tokens=[Coin(100, "uusdc"), Coin(100, "unusd")],
                # ),
                # # TODO fix: need usdc on-chain  to do this
                # pysdk.Msg.spot.swap(
                #     sender=sdk_agent.address,
                #     pool_id=pool_ids["unusd:uusdc"],
                #     token_in=Coin(100, "uusdc"),
                #     token_out_denom="unusd",
                # ),
                nibiru.Msg.spot.swap(
                    sender=client_validator.address,
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
def test_spot_exit_pool(client_validator):
    all_balance_maps = client_validator.query.get_bank_balances(
        client_validator.address
    )["balances"]

    balance_maps: List[Dict[Literal["denom", "amount"], Union[str, int]]] = [
        balance_map
        for balance_map in all_balance_maps
        if "pysdk.pool" in cast(str, balance_map["denom"])
    ]
    msgs: List[pytypes.PythonMsg] = []
    for pool_token in balance_maps:
        denom = pool_token.get("denom")
        assert isinstance(denom, str)

        pool_id = denom.split("/")[-1]
        assert isinstance(pool_id, str)

        amount = pool_token.get("amount")
        assert isinstance(amount, (str, int))
        msgs.append(
            nibiru.Msg.spot.exit_pool(
                sender=client_validator.address,
                pool_id=int(pool_id),
                pool_shares=Coin(int(amount), denom),
            )
        )
    if balance_maps:
        broadcast_resp = client_validator.tx.execute_msgs(msgs=msgs)
        tests.broadcast_tx_must_succeed(res=broadcast_resp)
    if not balance_maps:
        tests.LOGGER.info(
            "skipped test for 'nibid tx spot exit-pool' because\n"
            + f"{client_validator.address} did not have LP shares"
        )
