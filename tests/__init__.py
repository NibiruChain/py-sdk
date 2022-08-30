"""Tests package for the Nibiru Python SDK"""
import collections
import logging
import pprint
import sys
from typing import Any, Iterable, Optional, Union

import shutup

shutup.please()


class ColoredFormatter(logging.Formatter):

    fmt = "%(asctime)s|%(levelname)s|%(funcName)s| %(message)s"

    white = "\x1b[97;20m"
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    cyan = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: fmt.format(green, reset),
        logging.INFO: fmt.format(cyan, reset),
        logging.WARNING: fmt.format(yellow, reset),
        logging.ERROR: fmt.format(red, reset),
        logging.CRITICAL: fmt.format(bold_red, reset),
    }

    def format(self, record: logging.LogRecord):
        """Formats a record for the logging handler.

        Args:
            record (logging.LogRecord): Represents an instance of an event being
                logged.
        """
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format, datefmt="%H:%M:%S")
        return formatter.format(record=record)


def init_test_logger() -> logging.Logger:
    test_logger = logging.getLogger("test-logger")
    test_logger.setLevel(logging.DEBUG)

    # Logs to stdout so we can at least see logs in GHA.
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    handler.setFormatter(fmt=ColoredFormatter())
    test_logger.addHandler(handler)
    return test_logger


LOGGER: logging.Logger = init_test_logger()
"""Simple logger to use throughout the test suite."""


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


def dict_keys_must_match(dict_: dict, keys: list[str]):
    """Asserts that two iterables have the same elements, the same number of
    times, without regard to order.
    Alias for the 'element_counts_are_equal' function.

    dict_keys_must_match(dict_, keys)

    Example:
    - [0, 1, 1] and [1, 0, 1] compare equal.
    - [0, 0, 1] and [0, 1] compare unequal.

    """
    assert element_counts_are_equal(dict_.keys(), keys)


def transaction_must_succeed(tx_output: dict):
    """
    Ensure the output of a transaction have the fields required
    and that the raw logs are properly parsed

    Args:
        tx_output (dict): The output of a transaction in a dictionary
    """

    assert isinstance(tx_output, dict)
    dict_keys_must_match(
        tx_output,
        [
            "height",
            "txhash",
            "data",
            "rawLog",
            "logs",
            "gasWanted",
            "gasUsed",
            "events",
        ],
    )
    assert isinstance(tx_output["rawLog"], list)


def element_counts_are_equal(
    first: Iterable[Any], second: Iterable[Any]
) -> Optional[bool]:
    """Asserts that two iterables have the same elements, the same number of
    times, without regard to order.

    Args:
        first (Iterable[Any])
        second (Iterable[Any])

    Returns:
        Optional[bool]: "passed" status. If this is True, first and second share
            the same element counts. If they don't the function will raise an
            AssertionError and return 'None'.
    """
    first_seq, second_seq = list(first), list(second)

    passed: Union[bool, None]
    try:
        first = collections.Counter(first_seq)
        second = collections.Counter(second_seq)
    except TypeError:
        # Handle case with unhashable elements
        differences = _count_diff_all_purpose(first_seq, second_seq)
    else:
        if first == second:
            passed = True
            return passed
        differences = _count_diff_hashable(first_seq, second_seq)

    if differences:
        standardMsg = "Element counts were not equal:\n"
        lines = ["First has %d, Second has %d:  %r" % diff for diff in differences]
        diffMsg = "\n".join(lines)
        msg = "\n".join([standardMsg, diffMsg])
        passed = False
        assert passed, msg


_Mismatch = collections.namedtuple("Mismatch", "actual expected value")


def _count_diff_all_purpose(actual, expected):
    "Returns list of (cnt_act, cnt_exp, elem) triples where the counts differ"
    # elements need not be hashable
    s, t = list(actual), list(expected)
    m, n = len(s), len(t)
    NULL = object()
    result = []
    for i, elem in enumerate(s):
        if elem is NULL:
            continue
        cnt_s = cnt_t = 0
        for j in range(i, m):
            if s[j] == elem:
                cnt_s += 1
                s[j] = NULL
        for j, other_elem in enumerate(t):
            if other_elem == elem:
                cnt_t += 1
                t[j] = NULL
        if cnt_s != cnt_t:
            diff = _Mismatch(cnt_s, cnt_t, elem)
            result.append(diff)

    for i, elem in enumerate(t):
        if elem is NULL:
            continue
        cnt_t = 0
        for j in range(i, n):
            if t[j] == elem:
                cnt_t += 1
                t[j] = NULL
        diff = _Mismatch(0, cnt_t, elem)
        result.append(diff)
    return result


def _count_diff_hashable(actual, expected):
    "Returns list of (cnt_act, cnt_exp, elem) triples where the counts differ"
    # elements must be hashable
    s, t = collections.Counter(actual), collections.Counter(expected)
    result = []
    for elem, cnt_s in s.items():
        cnt_t = t.get(elem, 0)
        if cnt_s != cnt_t:
            diff = _Mismatch(cnt_s, cnt_t, elem)
            result.append(diff)
    for elem, cnt_t in t.items():
        if elem not in s:
            diff = _Mismatch(0, cnt_t, elem)
            result.append(diff)
    return result
