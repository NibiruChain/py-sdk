# bank_test.py

import nibiru
import tests
from nibiru import Coin

PRECISION = 6


def test_send_multiple_msgs(client_validator, client_new_user):
    """Tests the transfer of funds for a transaction with a multiple
    'MsgSend' tx messages.
    """
    tx_output = client_validator.tx.execute_msgs(
        msgs=[
            nibiru.Msg.bank.send(
                client_new_user.address,
                [Coin(7, "unibi"), Coin(70, "unusd")],
            ),
            nibiru.Msg.bank.send(
                client_new_user.address,
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


def test_send_single_msg(client_validator, client_new_user):
    """Tests the transfer of funds for a transaction with a single 'MsgSend'
    tx message.
    """

    tx_output = client_validator.tx.execute_msgs(
        [
            nibiru.Msg.bank.send(
                client_new_user.address,
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
