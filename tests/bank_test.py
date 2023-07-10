# bank_test.py

import pysdk
import tests
from pysdk import Coin

PRECISION = 6


def test_send_multiple_msgs(sdk_val: pysdk.Sdk, sdk_agent: pysdk.Sdk):
    """Tests the transfer of funds for a transaction with a multiple
    'MsgSend' tx messages.
    """
    tx_output = sdk_val.tx.execute_msgs(
        msgs=[
            pysdk.Msg.bank.send(
                sdk_val.address,
                sdk_agent.address,
                [Coin(7, "unibi"), Coin(70, "unusd")],
            ),
            pysdk.Msg.bank.send(
                sdk_val.address,
                sdk_agent.address,
                [Coin(15, "unibi"), Coin(23, "unusd")],
            ),
        ],
    )

    # TODO deprecated
    # tests.LOGGER.info(
    #     "nibid tx bank send - multiple msgs:\n" +
    #     tests.format_response(tx_output)
    # )
    tests.broadcast_tx_must_succeed(res=tx_output)
    tests.FullTxStory(broadcast_resp=tx_output).save()


def test_send_single_msg(sdk_val: pysdk.Sdk, sdk_agent: pysdk.Sdk):
    """Tests the transfer of funds for a transaction with a single 'MsgSend'
    tx message.
    """

    tx_output = sdk_val.tx.execute_msgs(
        [
            pysdk.Msg.bank.send(
                sdk_val.address,
                sdk_agent.address,
                [Coin(10, "unibi"), Coin(10, "unusd")],
            ),
        ]
    )

    # TODO deprecated
    # tests.LOGGER.info(
    #     "nibid tx bank send - single msgs:\n" +
    #     tests.format_response(tx_output)
    # )
    tests.broadcast_tx_must_succeed(res=tx_output)
    tests.FullTxStory(broadcast_resp=tx_output).save()
