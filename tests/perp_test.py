# perp_test.py
import pytest

import nibiru
import nibiru.msg
import tests
from nibiru import Coin, common
from nibiru.exceptions import QueryError
from tests import LOGGER, dict_keys_must_match, transaction_must_succeed

PRECISION = 6


def test_open_close_position(val_node: nibiru.Sdk, agent: nibiru.Sdk):
    """
    Open a position and ensure output is correct
    """
    pair = "ubtc:unusd"

    # Funding agent
    val_node.tx.execute_msgs(
        nibiru.msg.MsgSend(
            val_node.address, agent.address, [Coin(10000, "unibi"), Coin(100, "unusd")]
        )
    )

    # Exception must be raised when requesting not existing position
    with pytest.raises(QueryError, match="not found: 'nibiru.perp.v1.Position'"):
        agent.query.perp.position(trader=agent.address, token_pair=pair)

    # Transaction open_position must succeed
    tx_output: dict = agent.tx.execute_msgs(
        nibiru.msg.MsgOpenPosition(
            sender=agent.address,
            token_pair=pair,
            side=common.Side.BUY,
            quote_asset_amount=10,
            leverage=10,
            base_asset_amount_limit=0,
        )
    )
    LOGGER.info(f"nibid tx perp open-position: {tests.format_response(tx_output)}")
    transaction_must_succeed(tx_output)

    # Trader position must be a dict with specific keys
    position_res = agent.query.perp.position(trader=agent.address, token_pair=pair)
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
    LOGGER.info(
        f"nibid query perp trader-position: \n{tests.format_response(position_res)}"
    )
    # Margin ratio must be ~10%
    assert position_res["margin_ratio_mark"] == pytest.approx(0.1, PRECISION)

    position = position_res["position"]
    assert position["margin"] == 10.0
    assert position["open_notional"] == 100.0
    assert position["size"] == pytest.approx(0.005, PRECISION)

    # Transaction add_margin must succeed
    tx_output = agent.tx.execute_msgs(
        nibiru.msg.MsgAddMargin(
            sender=agent.address,
            token_pair=pair,
            margin=Coin(10, "unusd"),
        )
    )
    LOGGER.info(f"nibid tx perp add-margin: \n{tests.format_response(tx_output)}")
    transaction_must_succeed(tx_output)

    # Margin must increase. 10 + 10 = 20
    position = agent.query.perp.position(trader=agent.address, token_pair=pair)[
        "position"
    ]
    assert position["margin"] == 20.0

    # Transaction remove_margin must succeed
    tx_output = agent.tx.execute_msgs(
        nibiru.msg.MsgRemoveMargin(
            sender=agent.address,
            token_pair=pair,
            margin=common.Coin(5, "unusd"),
        )
    )
    LOGGER.info(f"nibid tx perp remove-margin: \n{tests.format_response(tx_output)}")
    transaction_must_succeed(tx_output)

    # Margin must decrease. 20 - 5 = 15
    position = agent.query.perp.position(trader=agent.address, token_pair=pair)[
        "position"
    ]
    assert position["margin"] == 15.0

    # Transaction close_position must succeed
    tx_output = agent.tx.execute_msgs(
        nibiru.msg.MsgClosePosition(sender=agent.address, token_pair=pair)
    )
    LOGGER.info(f"nibid tx perp close-position: \n{tests.format_response(tx_output)}")
    transaction_must_succeed(tx_output)

    # Exception must be raised when querying closed position
    with pytest.raises(QueryError, match="not found: 'nibiru.perp.v1.Position'"):
        agent.query.perp.position(trader=agent.address, token_pair=pair)
