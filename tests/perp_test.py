# perp_test.py
from ast import List
from typing import Optional

import pytest

import nibiru
import nibiru.msg
import tests
from nibiru import Coin, pytypes
from nibiru.exceptions import QueryError
from tests import LOGGER, dict_keys_must_match, transaction_must_succeed

PRECISION = 6

PAIR = "ubtc:unusd"


def give_agent_funds(
    val_node: nibiru.Sdk, agent: nibiru.Sdk
) -> Optional[pytypes.RawTxResp]:
    # Funding agent
    tests.LOGGER.info(
        "\n".join(
            [f"nibid tx bank send", f"from: {val_node.address}", f"to: {agent.address}"]
        )
    )
    return val_node.tx.execute_msgs(
        nibiru.msg.MsgSend(
            from_address=val_node.address,
            to_address=agent.address,
            coins=[Coin(10000, "unibi"), Coin(100, "unusd")],
        )
    )


@pytest.fixture
def test_open_position(val_node: nibiru.Sdk, agent: nibiru.Sdk) -> bool:
    assert give_agent_funds(val_node=val_node, agent=agent), "failed to fund the agent"

    tx_output: dict = val_node.tx.execute_msgs(
        nibiru.msg.MsgOpenPosition(
            sender=val_node.address,
            token_pair=PAIR,
            side=pytypes.Side.BUY,
            quote_asset_amount=10,
            leverage=10,
            base_asset_amount_limit=0,
        )
    )
    LOGGER.info(f"nibid tx perp open-position: {tests.format_response(tx_output)}")
    transaction_must_succeed(tx_output)

    tx_resp = pytypes.TxResp.from_raw(pytypes.RawTxResp(tx_output))
    assert "/nibiru.perp.v1.MsgOpenPosition" in tx_resp.rawLog[0].msgs
    events_for_msg: List[str] = [
        "nibiru.perp.v1.PositionChangedEvent",
        "nibiru.vpool.v1.SwapQuoteForBaseEvent",
        "nibiru.vpool.v1.MarkPriceChangedEvent",
        "transfer",
    ]
    assert all(
        [msg_event in tx_resp.rawLog[0].event_types for msg_event in events_for_msg]
    )
    breakpoint()

    # Trader position must be a dict with specific keys
    position_res = agent.query.perp.position(trader=agent.address, token_pair=PAIR)
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

    assert position_res["margin_ratio_mark"]
    position = position_res["position"]
    assert position["margin"]
    assert position["open_notional"]
    assert position["size"]
    return True


def test_open_close_position(test_open_position: bool, agent: nibiru.Sdk):
    """
    Open a position and ensure output is correct
    """
    assert test_open_position, "failed to open position"

    # Transaction add_margin must succeed
    tx_output = agent.tx.execute_msgs(
        nibiru.msg.MsgAddMargin(
            sender=agent.address,
            token_pair=PAIR,
            margin=Coin(10, "unusd"),
        )
    )
    LOGGER.info(f"nibid tx perp add-margin: \n{tests.format_response(tx_output)}")
    transaction_must_succeed(tx_output)

    # Margin must increase. 10 + 10 = 20
    position = agent.query.perp.position(trader=agent.address, token_pair=PAIR)[
        "position"
    ]
    assert position["margin"] == 20.0

    # Transaction remove_margin must succeed
    tx_output = agent.tx.execute_msgs(
        nibiru.msg.MsgRemoveMargin(
            sender=agent.address,
            token_pair=PAIR,
            margin=pytypes.Coin(5, "unusd"),
        )
    )
    LOGGER.info(f"nibid tx perp remove-margin: \n{tests.format_response(tx_output)}")
    transaction_must_succeed(tx_output)

    # Margin must decrease. 20 - 5 = 15
    position = agent.query.perp.position(trader=agent.address, token_pair=PAIR)[
        "position"
    ]
    assert position["margin"] == 15.0

    # Transaction close_position must succeed
    tx_output = agent.tx.execute_msgs(
        nibiru.msg.MsgClosePosition(sender=agent.address, token_pair=PAIR)
    )
    LOGGER.info(f"nibid tx perp close-position: \n{tests.format_response(tx_output)}")
    transaction_must_succeed(tx_output)

    # Exception must be raised when querying closed position
    with pytest.raises(QueryError, match="not found: 'nibiru.perp.v1.Position'"):
        agent.query.perp.position(trader=agent.address, token_pair=PAIR)
