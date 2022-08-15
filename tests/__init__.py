"""Tests for the nibiru-py package"""
import dataclasses
import os
import unittest
from typing import List

import dotenv
import pytest

import nibiru
from nibiru import common
from nibiru.common import Coin

dotenv.load_dotenv()


@dataclasses.dataclass
class TestConfig:
    LCD_PORT = "1317"
    GRPC_PORT = "9090"
    VALIDATOR_MNEMONIC = os.environ["VALIDATOR_MNEMONIC"]
    ORACLE_MNEMONIC = os.environ["ORACLE_MNEMONIC"]
    NETWORK_INSECURE = os.environ["NETWORK_INSECURE"]
    CHAIN_ID = os.environ["CHAIN_ID"]
    HOST = os.environ["HOST"]


CONFIG = TestConfig()


class ModuleTest(unittest.TestCase):
    def setUp(self):
        self.validator = get_val_node(get_network())
        self.market = "ubtc:unusd"

    def validate_tx_output(self, tx_output: dict):
        """
        Ensure the output of a transaction have the fields required and that the raw logs are properly parsed

        Args:
            tx_output (dict): The output of a transaction in a dictionary
        """

        self.assertIsInstance(tx_output, dict)
        self.assertCountEqual(
            tx_output.keys(),
            [
                'height',
                'txhash',
                'data',
                'rawLog',
                'logs',
                'gasWanted',
                'gasUsed',
                'events',
            ],
        )
        self.assertIsInstance(tx_output["rawLog"], list)

    def create_new_agent_with_funds(self, coins: List[Coin]) -> nibiru.Sdk:
        """
        Create a new agent and fund it from the validator with some funds

        Args:
            coins (List[Coin]): A list of coins to fund

        Returns:
            (nibiru.Sdk): The new agent
        """
        tx_config = nibiru.TxConfig(tx_type=common.TxType.BLOCK)
        agent = (
            nibiru.Sdk.authorize()
            .with_config(tx_config)
            .with_network(get_network(), CONFIG.NETWORK_INSECURE)
        )

        result = self.validator.tx.msg_send(
            self.validator.address, agent.address, coins
        )
        self.validate_tx_output(result)

        return agent


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
    return (
        nibiru.Sdk.authorize(CONFIG.VALIDATOR_MNEMONIC)
        .with_config(tx_config)
        .with_network(network, CONFIG.NETWORK_INSECURE)
    )


def get_oracle_node(network: nibiru.Network) -> nibiru.Sdk:
    tx_config = nibiru.TxConfig(tx_type=common.TxType.BLOCK, gas_multiplier=3)
    return (
        nibiru.Sdk.authorize(CONFIG.ORACLE_MNEMONIC)
        .with_config(tx_config)
        .with_network(network, CONFIG.NETWORK_INSECURE)
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
