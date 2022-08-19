"""Tests for the nibiru package"""
import logging
import sys

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
