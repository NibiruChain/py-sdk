# perp_test.py
from _pytest.python_api import approx
from grpc._channel import _InactiveRpcError
from pytest import raises

import nibiru
from nibiru import Coin, common
from tests import dict_keys_must_match, transaction_must_succeed

PRECISION = 6


def test_open_close_position(val_node: nibiru.Sdk, agent: nibiru.Sdk):
    """
    Open a position and ensure output is correct
    """
    pair = "ubtc:unusd"

    # Funding agent
    val_node.tx.msg_send(
        val_node.address, agent.address, [Coin(10000, "unibi"), Coin(100, "unusd")]
    )

    # Exception must be raised when requesting not existing position
    with raises(_InactiveRpcError, match="no position found"):
        agent.query.perp.trader_position(trader=agent.address, token_pair=pair)

    # Transaction open_position must succeed
    tx_output = agent.tx.perp.open_position(
        sender=agent.address,
        token_pair=pair,
        side=common.Side.BUY,
        quote_asset_amount=10,
        leverage=10,
        base_asset_amount_limit=0,
    )
    transaction_must_succeed(tx_output)

    # Trader position must be a dict with specific keys
    position_res = agent.query.perp.trader_position(
        trader=agent.address, token_pair=pair
    )
    dict_keys_must_match(
        position_res,
        [
            "block_number",
            "margin_ratio_index",
            "margin_ratio_mark",
            "position",
            "position_notional",
            "unrealized_pnl",
        ],
    )
    # Margin ratio must be ~10%
    assert position_res["margin_ratio_mark"] == approx(0.1, PRECISION)

    position = position_res["position"]
    assert position["margin"] == 10.0
    assert position["open_notional"] == 100.0
    assert position["size"] == approx(0.005, PRECISION)

    # Transaction add_margin must succeed
    tx_output = agent.tx.perp.add_margin(
        sender=agent.address,
        token_pair=pair,
        margin=Coin(10, "unusd"),
    )
    transaction_must_succeed(tx_output)

    # Margin must increase. 10 + 10 = 20
    position = agent.query.perp.trader_position(trader=agent.address, token_pair=pair)[
        "position"
    ]
    assert position["margin"] == 20.0

    # Transaction remove_margin must succeed
    tx_output = agent.tx.perp.remove_margin(
        sender=agent.address,
        token_pair=pair,
        margin=common.Coin(5, "unusd"),
    )
    transaction_must_succeed(tx_output)

    # Margin must decrease. 20 - 5 = 15
    position = agent.query.perp.trader_position(trader=agent.address, token_pair=pair)[
        "position"
    ]
    assert position["margin"] == 15.0

    # Transaction close_position must succeed
    tx_output = agent.tx.perp.close_position(sender=agent.address, token_pair=pair)
    transaction_must_succeed(tx_output)

    # Exception must be raised when querying closed position
    with raises(_InactiveRpcError, match="no position found"):
        agent.query.perp.trader_position(trader=agent.address, token_pair=pair)
