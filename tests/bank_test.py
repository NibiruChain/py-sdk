# bank_test.py

import nibiru
import tests
from nibiru import Coin

PRECISION = 6


def test_send_multiple_msgs(sdk_val: nibiru.Sdk, sdk_agent: nibiru.Sdk):
    """Tests the transfer of funds for a transaction with a multiple
    'MsgSend' tx messages.
    """
    tx_output = sdk_val.tx.execute_msgs(
        msgs=[
            nibiru.Msg.bank.send(
                sdk_val.address,
                sdk_agent.address,
                [Coin(7, "unibi"), Coin(70, "unusd")],
            ),
            nibiru.Msg.bank.send(
                sdk_val.address,
                sdk_agent.address,
                [Coin(15, "unibi"), Coin(23, "unusd")],
            ),
        ],
    )

    tests.LOGGER.info(
        "nibid tx bank send - multiple msgs:\n" + tests.format_response(tx_output)
    )
    tests.raw_sync_tx_must_succeed(tx_output)


def test_send_single_msg(sdk_val: nibiru.Sdk, sdk_agent: nibiru.Sdk):
    """Tests the transfer of funds for a transaction with a single 'MsgSend'
    tx message.
    """

    tx_output = sdk_val.tx.execute_msgs(
        [
            nibiru.Msg.bank.send(
                sdk_val.address,
                sdk_agent.address,
                [Coin(10, "unibi"), Coin(10, "unusd")],
            ),
        ]
    )

    tests.LOGGER.info(
        "nibid tx bank send - single msgs:\n" + tests.format_response(tx_output)
    )
    tests.raw_sync_tx_must_succeed(tx_output)
