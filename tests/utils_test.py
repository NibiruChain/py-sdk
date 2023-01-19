import subprocess
from typing import List
from urllib.parse import ParseResult, urlparse

import pytest
from nibiru_proto.cosmos.bank.v1beta1 import MsgSend
from nibiru_proto.nibiru.perp.v1 import MsgOpenPosition

import nibiru
import tests
from nibiru import Coin, pytypes
from nibiru.query_clients.util import get_block_messages, get_msg_pb_by_type_url
from nibiru.utils import from_sdk_dec, to_sdk_dec


@pytest.mark.parametrize(
    "test_name,float_val,sdk_dec_val,should_fail",
    [
        ('empty string', '', '', True),
        # valid numbers
        ('number 0', 0, '0' + '0' * 18, False),
        ('number 10', 10, '10' + '0' * 18, False),
        ('number 123', 123, '123' + '0' * 18, False),
        ('neg. number 123', -123, '-123' + '0' * 18, False),
        # with fractional
        ('missing mantisse', 0.3, '03' + '0' * 17, False),
        ('number 0.5', 0.5, '05' + '0' * 17, False),
        ('number 13.235', 13.235, '13235' + '0' * 15, False),
        ('neg. number 13.235', -13.235, '-13235' + '0' * 15, False),
        ('number 1574.00005', 1574.00005, '157400005' + '0' * 13, False),
    ],
)
def test_to_sdk_dec(test_name, float_val, sdk_dec_val, should_fail):
    try:
        res = to_sdk_dec(float_val)
        assert sdk_dec_val == res
        assert not should_fail
    except (TypeError, ValueError):
        assert should_fail


@pytest.mark.parametrize(
    "test_name,sdk_dec_val,float_val,should_fail",
    [
        ('number with \'.\'', '.3', '', True),
        ('number with \'.\'', '5.3', '', True),
        ('invalid number', 'hello', '', True),
        # valid numbers
        ('empty string', '', 0, False),
        ('empty string', None, 0, False),
        ('number 0', '0' * 5, 0, False),
        ('number 0', '0' * 22, 0, False),
        ('number 10', '10' + '0' * 18, 10, False),
        ('neg. number 10', '-10' + '0' * 18, -10, False),
        ('number 123', '123' + '0' * 18, 123, False),
        # with fractional
        ('number 0.5', '05' + '0' * 17, 0.5, False),
        ('fractional only 0.00596', '596' + '0' * 13, 0.00596, False),
        ('number 13.5', '135' + '0' * 17, 13.5, False),
        ('neg. number 13.5', '-135' + '0' * 17, -13.5, False),
        ('number 1574.00005', '157400005' + '0' * 13, 1574.00005, False),
    ],
)
def test_from_sdk_dec(test_name, sdk_dec_val, float_val, should_fail):
    try:
        res = from_sdk_dec(sdk_dec_val)
        assert float_val == res
        assert not should_fail
    except (TypeError, ValueError):
        assert should_fail


@pytest.mark.parametrize(
    "type_url,cls",
    [
        ("/nibiru.perp.v1.MsgOpenPosition", MsgOpenPosition),
        ("/cosmos.bank.v1beta1.MsgSend", MsgSend),
    ],
)
def test_get_msg_pb_by_type_url(type_url, cls):
    assert get_msg_pb_by_type_url(type_url) == cls()


def test_get_block_messages(sdk_val: nibiru.Sdk, sdk_agent: nibiru.Sdk):
    tx_output: pytypes.RawTxResp = sdk_val.tx.execute_msgs(
        nibiru.Msg.bank.send(
            sdk_val.address,
            sdk_agent.address,
            [Coin(10000, "unibi"), Coin(100, "unusd")],
        )
    )
    height = int(tx_output["height"])
    block_resp = sdk_agent.query.get_block_by_height(height)
    messages: List[dict] = get_block_messages(block_resp.block)

    msg = messages[0]
    assert isinstance(msg, dict)
    assert msg["type_url"] == "/cosmos.bank.v1beta1.MsgSend"
    tests.dict_keys_must_match(
        msg["value"],
        ["from_address", "to_address", "amount"],
    )


def can_ping(host) -> bool:
    """
    Check wether the host can be pinged.

    Args:
        host (str): the url of the host to ping

    Returns:
        bool: wether we can ping or not
    """
    ping = subprocess.Popen(
        ["ping", "-c", "4", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    _, error = ping.communicate()
    return error == b""


def url_to_host(url: str) -> str:
    """
    Convert an url like "https://rpc.devnet-2.nibiru.fi:443" to "https://rpc.devnet-2.nibiru.fi"

    Args:
        url (str): tue url to transform

    Returns:
        str: an url that can be pinged
    """
    url: ParseResult = urlparse(url)

    if url.scheme == 'localhost':
        return url.scheme

    assert url.hostname, ReferenceError(f"Url {url} hostname is empty.")

    return url.hostname
