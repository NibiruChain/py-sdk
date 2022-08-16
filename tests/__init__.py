"""Tests for the nibiru package"""
import logging
import sys

logging.basicConfig()

def init_test_logger() -> logging.Logger:
    test_logger = logging.getLogger("test-logger")
    test_logger.setLevel(logging.DEBUG)

    # Logs to stdout so we can at least see logs in GHA.
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    test_logger.addHandler(handler)
    return test_logger

LOGGER = init_test_logger()
"""Simple logger to use throughout the test suite."""

def dict_keys_must_match(dict_: dict, keys: list[str]):
    assert len(dict_.keys()) == len(keys)
    for key in dict_.keys():
        assert key in keys


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
