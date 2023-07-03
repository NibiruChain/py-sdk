"""Tests package for the Nibiru Python SDK"""
import sys

sys.path.append(
    "/Users/anishpalvai/Library/Caches/pypoetry/virtualenvs/nibiru-tfKa6q6O-py3.8/lib/python3.8/site-packages/nibiru_proto/nibiru"
)
sys.path.append(
    "/Users/anishpalvai/Library/Caches/pypoetry/virtualenvs/nibiru-tfKa6q6O-py3.8/lib/python3.8/site-packages/nibiru_proto/nibiru/epochs"
)
sys.path.append(
    "/Users/anishpalvai/Library/Caches/pypoetry/virtualenvs/nibiru-tfKa6q6O-py3.8/lib/python3.8/site-packages/nibiru_proto/nibiru/epochs/v1"
)
print(sys.path)

import logging
import pprint
from typing import Iterable, List, Union

import shutup

from nibiru import utils

shutup.please()

LOGGER: logging.Logger = logging.getLogger("test-logger")


def raises(errs: Union[str, Iterable[str]], err: BaseException):
    """Makes sure one of the errors in 'errs' in contained in 'err'. If none of
    the given exceptions were raised, this function raises the original exception.

    Args:
        errs (Union[str, Iterable[str]]): An error string or iterable of error
            strings, of which we expect one to be contained in 'err'.
        err: (BaseException): The error that is actually raised.

    """
    if isinstance(errs, str):
        errs = [errs]
    else:
        errs = list(errs)
    errs: List[str]

    err_string = str(err)
    assert any([e in err_string for e in errs]), err_string


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
