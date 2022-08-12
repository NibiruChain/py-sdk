"""Tests for the nibiru-py package"""
import dataclasses
import os

import dotenv
import pytest

import nibiru
from nibiru import common

dotenv.load_dotenv()


@dataclasses.dataclass
class TestConfig:
    LCD_PORT = "1317"
    GRPC_PORT = "9090"
    VALIDATOR_MNEMONIC = os.environ["VALIDATOR_MNEMONIC"]
    CHAIN_ID = os.environ["CHAIN_ID"]
    HOST = os.environ["HOST"]


CONFIG = TestConfig()


def get_network() -> nibiru.Network:
    return nibiru.Network(
        lcd_endpoint=f'http://{CONFIG.HOST}:{CONFIG.LCD_PORT}',
        grpc_endpoint=f'{CONFIG.HOST}:{CONFIG.GRPC_PORT}',
        chain_id=CONFIG.CHAIN_ID,
        fee_denom='unibi',
        env="local",
    )


def get_val_node(network: nibiru.Network) -> nibiru.Sdk:
    tx_config = nibiru.TxConfig(tx_type=common.TxType.BLOCK)
    newtork_insecure: bool = True
    return (
        nibiru.Sdk.authorize(CONFIG.VALIDATOR_MNEMONIC).with_config(tx_config).with_network(network, newtwork_insecure)
    )


@pytest.fixture
def network() -> nibiru.Network:
    """
    Generate a network object

    Returns:
        nibiru.Network: Nibiru network object
    """
    return get_network()


@pytest.fixture
def val_node(network: nibiru.Network) -> nibiru.Sdk:
    """
    Create a authorized sdk with the validator mnemonic.

    Args:
        network (nibiru.Network): A nibiru network object

    Returns:
        nibiru.Sdk: The sdk object valid
    """
    return get_val_node(network)
