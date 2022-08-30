# bank_test.py

import nibiru
import nibiru.msg
import tests
from nibiru import Coin

PRECISION = 6


def test_send_multiple_msgs(val_node: nibiru.Sdk, agent: nibiru.Sdk):
    """Tests the transfer of funds for a transaction with a multiple 'MsgSend' messages."""

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

    tests.LOGGER.info(
        "nibid tx bank send - multiple msgs:\n" + tests.format_response(tx_output)
    )
    tests.transaction_must_succeed(tx_output)


def test_send_single_msg(val_node: nibiru.Sdk, agent: nibiru.Sdk):
    """Tests the transfer of funds for a transaction with a single 'MsgSend' message."""

    tx_output = val_node.tx.execute_msgs(
        [
            nibiru.msg.MsgSend(
                val_node.address,
                agent.address,
                [Coin(10000, "unibi"), Coin(100, "unusd")],
            ),
        ]
    )

    tests.LOGGER.info(
        "nibid tx bank send - single msgs:\n" + tests.format_response(tx_output)
    )
    tests.transaction_must_succeed(tx_output)
