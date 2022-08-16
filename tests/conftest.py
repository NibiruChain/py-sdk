"""
conftest.py is a special file that contains global fixture functions to be used
in tests. All test modules in the current (and child) directories can access
these fixtures.

See "Scope: sharing fixtures across classes, modules, packages or session"
- docs reference: https://docs.pytest.org/en/6.2.x/fixture.html

Fixtures available:
- network
- val_node
- oracle_node
- agent_node
"""
import os

import pytest
from dotenv import load_dotenv

from nibiru import Network, Sdk
from nibiru.common import Coin, TxConfig, TxType


def pytest_configure(config):
    load_dotenv()

    expected_env_vars = (
        "HOST",
        "GRPC_PORT",
        "LCD_PORT",
        "CHAIN_ID",
        "VALIDATOR_MNEMONIC",
        "ORACLE_MNEMONIC",
    )
    for var in expected_env_vars:
        if not os.getenv(var):
            raise ValueError(f"Environment variable {var} is missing!")

    pytest.VALIDATOR_MNEMONIC = os.getenv("VALIDATOR_MNEMONIC")
    pytest.ORACLE_MNEMONIC = os.getenv("ORACLE_MNEMONIC")
    pytest.NETWORK_INSECURE = os.getenv("NETWORK_INSECURE") != "false"

@pytest.fixture
def network() -> Network:
    return Network.devnet()


@pytest.fixture
def val_node(network: Network) -> Sdk:
    tx_config = TxConfig(tx_type=TxType.BLOCK)

    return (
        Sdk.authorize(pytest.VALIDATOR_MNEMONIC)
        .with_config(tx_config)
        .with_network(network, pytest.NETWORK_INSECURE)
    )


@pytest.fixture
def oracle_agent(network: Network, val_node: Sdk) -> Sdk:
    tx_config = TxConfig(tx_type=TxType.BLOCK, gas_multiplier=3)
    agent = (
        Sdk.authorize(os.getenv("ORACLE_MNEMONIC"))
        .with_config(tx_config)
        .with_network(network, pytest.NETWORK_INSECURE)
    )
    val_node.tx.msg_send(val_node.address, agent.address, [Coin(10000, "unibi")])
    return agent


@pytest.fixture
def agent(network: Network) -> Sdk:
    tx_config = TxConfig(tx_type=TxType.BLOCK, gas_multiplier=3)
    return (
        Sdk.authorize()
        .with_config(tx_config)
        .with_network(network, pytest.NETWORK_INSECURE)
    )
