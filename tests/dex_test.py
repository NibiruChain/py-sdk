# perp_test.py

import nibiru
import nibiru.msg
from nibiru import Coin, PoolAsset
from nibiru.exceptions import SimulationError
from nibiru.pytypes import PoolType
from tests import transaction_must_succeed

PRECISION = 6


def test_dex(val_node: nibiru.Sdk, agent: nibiru.Sdk):
    """
    Test the workflow for pools
    """
    try:
        tx_output = val_node.tx.execute_msgs(
            nibiru.msg.MsgCreatePool(
                creator=val_node.address,
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
        assert "a pool with the same denoms already exists" in str(simulation_error)

    try:
        tx_output = val_node.tx.execute_msgs(
            nibiru.msg.MsgCreatePool(
                creator=val_node.address,
                swap_fee=0.01,
                exit_fee=0.02,
                assets=[
                    PoolAsset(token=Coin(100, "uusdc"), weight=50),
                    PoolAsset(token=Coin(1000, "unusd"), weight=50),
                ],
                pool_type=PoolType.STABLESWAP,
                a=10,
            )
        )
        transaction_must_succeed(tx_output)
    except SimulationError as simulation_error:
        assert "a pool with the same denoms already exists" in str(simulation_error)

    # Assert pool are there.
    pools = val_node.query.dex.pools()
    pool_ids = {}
    for pool_assets in ["unibi:unusd", "uusdc:unusd"]:
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

        pool_ids[pool_assets] = int(
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

    # Join/swap/exit pool
    tx_output = val_node.tx.execute_msgs(
        nibiru.msg.MsgSend(
            val_node.address,
            agent.address,
            [Coin(10000, "unibi"), Coin(200, "unusd"), Coin(200, "uusdc")],
        )
    )
    transaction_must_succeed(tx_output)

    pools = val_node.query.dex.pools()

    tx_output = agent.tx.execute_msgs(
        [
            nibiru.msg.MsgJoinPool(
                sender=agent.address,
                pool_id=pool_ids["unibi:unusd"],
                tokens=[Coin(1000, "unibi"), Coin(100, "unusd")],
            ),
            nibiru.msg.MsgJoinPool(
                sender=agent.address,
                pool_id=pool_ids["uusdc:unusd"],
                tokens=[Coin(100, "uusdc"), Coin(100, "unusd")],
            ),
            nibiru.msg.MsgSwapAssets(
                sender=agent.address,
                pool_id=pool_ids["uusdc:unusd"],
                token_in=Coin(100, "uusdc"),
                token_out_denom="unusd",
            ),
            nibiru.msg.MsgSwapAssets(
                sender=agent.address,
                pool_id=pool_ids["unibi:unusd"],
                token_in=Coin(100, "unibi"),
                token_out_denom="unusd",
            ),
        ]
    )
    transaction_must_succeed(tx_output)

    balance = agent.query.get_bank_balances(agent.address)["balances"]

    tx_output = agent.tx.execute_msgs(
        [
            nibiru.msg.MsgExitPool(
                sender=agent.address,
                pool_id=int(pool_token["denom"].split("/")[-1]),
                pool_shares=Coin(pool_token["amount"], pool_token["denom"]),
            )
            for pool_token in balance
            if "nibiru/pool" in pool_token["denom"]
        ]
    )
