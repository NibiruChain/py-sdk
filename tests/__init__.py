"""Tests package for the pysdk.Python SDK"""
import dataclasses
import logging
import os
import pprint
from typing import Iterable, List, Optional, Union

# mypy skips analysis when there's a "type: ignore" comment.
# This is used when we want to skip static analysis because of missing library
# stubs or py.typed marker.
# NOTE: See https://mypy.readthedocs.io/en/stable/running_mypy.html#mis
import shutup  # type: ignore

from nibiru import Network, PrivateKey, utils
from nibiru.chain_client import ChainClient
from nibiru.pytypes import common, tx_resp
from nibiru_proto.cosmos.tx.v1beta1 import service_pb2 as tx_service  # type: ignore

shutup.please()

LOGGER: logging.Logger = logging.getLogger("test-logger")


def raises(ok_errs: Union[str, Iterable[str]], err: BaseException):
    """Makes sure one of the errors in 'errs' in contained in 'err'. If none of
    the given exceptions were raised, this function raises the original exception.

    Args:
        errs (Union[str, Iterable[str]]): An error string or iterable of error
            strings, of which we expect one to be contained in 'err'.
        err: (BaseException): The error that is actually raised.

    """
    if isinstance(ok_errs, str):
        ok_errs = [ok_errs]
    else:
        ok_errs = list(ok_errs)
    assert isinstance(ok_errs, list)
    # ok_errs: List[str]

    err_string = str(err)
    assert any([e in err_string for e in ok_errs]), err_string


def format_response(resp: Union[dict, list, str]) -> str:
    """Pretty formats a query or transaction response

    Args:
        resp (Union[dict, list, str]): A query or transaction response.

    Raises:
        TypeError: If 'resp' is not a dict or list.

    Returns:
        str: pretty version of the response
    """
    if not isinstance(resp, (list, dict, str)):
        raise TypeError(f"'resp' has invalid type {type(resp)}")

    if isinstance(resp, dict) and "logs" in resp:
        return pprint.pformat(resp.get("logs"), indent=3)
    else:
        return pprint.pformat(resp, indent=3)


def dict_keys_must_match(dict_: dict, keys: Iterable[str]):
    """Asserts that two iterables have the same elements, the same number of
    times, without regard to order. This function is asserts the output of the
    'element_counts_are_equal' function.

    Args:
        dict_ (dict): The dictionary that's having its keys checked.
        keys (Iterable[str]): An iterable of keys that that 'dict_' should have.

    Examples:

    ```python
    # no error
    dict_keys_must_match(dict_={"a": 0, "b": 1}, keys=["a", "b"])
    # raises error
    dict_keys_must_match(dict_={"a": 0, "b": 1}, keys=["a"])
    ```
    """
    assert utils.element_counts_are_equal(dict_.keys(), keys)


def transaction_must_succeed(tx_output: dict):
    """
    Ensure the output of a transaction have the fields required
    and that the raw logs are properly parsed

    Args:
        tx_output (dict): The output of a transaction in a dictionary
    """

    assert isinstance(tx_output, dict)
    expected_keys = ["height", "txhash", "data", "rawLog", "logs", "gasWanted"] + [
        "gasUsed",
        "events",
    ]
    dict_keys_must_match(tx_output, expected_keys)
    assert isinstance(tx_output["rawLog"], list)


def broadcast_tx_must_succeed(res: tx_resp.ExecuteTxResp):
    """
    Ensure the output of a transaction have the fields required
    and that the raw logs are properly parsed

    Args:
        tx_output (dict): The output of a transaction in a dictionary
    """

    assert isinstance(res, tx_resp.ExecuteTxResp)
    assert res.code == 0
    assert res.tx_hash


def raw_sync_tx_must_succeed(tx_output: dict):
    """
    Ensure the output of a transaction have the fields required
    and that the raw logs are properly parsed

    Args:
        tx_output (dict): The output of a transaction in a dictionary
    """

    assert isinstance(tx_output, dict)
    expected_keys = ["txhash", "rawLog"]
    dict_keys_must_match(tx_output, expected_keys)
    assert isinstance(tx_output["rawLog"], list)


TX_CONFIG_TEST: common.TxConfig = common.TxConfig(
    broadcast_mode=common.TxBroadcastMode.SYNC,
    gas_multiplier=1.25,
    gas_price=0.25,
)


def fixture_network() -> Network:
    return Network.customnet()


def fixture_client_validator() -> ChainClient:
    client = ChainClient(
        network=fixture_network(),
        tx_config=TX_CONFIG_TEST,
    )
    client.authenticate(mnemonic=os.getenv("VALIDATOR_MNEMONIC"))
    return client


def fixture_client_new_user() -> ChainClient:
    client = ChainClient(
        network=fixture_network(),
        tx_config=TX_CONFIG_TEST,
    )
    mnemonic, private_key = PrivateKey.generate()
    client.authenticate(mnemonic=mnemonic)
    return client


@dataclasses.dataclass
class FullTxStory:
    broadcast_resp: tx_resp.ExecuteTxResp
    query_tx_resp: Optional[tx_service.GetTxResponse] = None

    def save(self):
        FULL_TX_STORIES.append(self)


FULL_TX_STORIES: List[FullTxStory] = []
