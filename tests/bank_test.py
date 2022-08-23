# bank_test.py

import nibiru
import nibiru.msg
from nibiru import Coin
from tests import transaction_must_succeed

PRECISION = 6


def test_send_multiple_txs(val_node: nibiru.Sdk, agent: nibiru.Sdk):
    """
    Open a position and ensure output is correct
    """

    # Funding agent

    tx_output = val_node.tx.execute_msgs(
        [
            nibiru.msg.MsgSend(
                val_node.address,
                agent.address,
                [Coin(10000, "unibi"), Coin(100, "unusd")],
            ),
            nibiru.msg.MsgSend(
                val_node.address,
                agent.address,
                [Coin(10000, "unibi"), Coin(100, "unusd")],
            ),
        ]
    )

    transaction_must_succeed(tx_output)


def test_send_multiple_txs_with_fail(val_node: nibiru.Sdk, agent: nibiru.Sdk):
    """
    Open a position and ensure output is correct
    """

    # Funding agent
    pair = "ubtc:unusd"

    tx_output = val_node.tx.execute_msgs(
        [
            nibiru.msg.MsgSend(
                val_node.address,
                agent.address,
                [Coin(10000, "unibi"), Coin(100, "unusd")],
            ),
            nibiru.msg.MsgOpenPosition(
                sender=val_node.address,
                token_pair=pair,
                side=nibiru.Side.BUY,
                quote_asset_amount=10,
                leverage=10,
                base_asset_amount_limit=0,
            ),
            nibiru.msg.MsgLiquidate(
                sender=val_node.address,
                token_pair=pair,
                trader=val_node.address,
            ),
        ]
    )

    transaction_must_succeed(tx_output)


def test_send_single_tx(val_node: nibiru.Sdk, agent: nibiru.Sdk):
    """
    Open a position and ensure output is correct
    """

    # Funding agent

    tx_output = val_node.tx.execute_msgs(
        [
            nibiru.msg.MsgSend(
                val_node.address,
                agent.address,
                [Coin(10000, "unibi"), Coin(100, "unusd")],
            ),
        ]
    )

    transaction_must_succeed(tx_output)
