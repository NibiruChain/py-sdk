"""
conftest.py is a special file that contains global fixture functions to be used
in tests. All test modules in the current (and child) directories can access
these fixtures.

See "Scope: sharing fixtures across classes, modules, packages or session"
- docs reference: https://docs.pytest.org/en/6.2.x/fixture.html

Fixtures available:
- network
- val_node
- agent_node
"""
import os
from typing import List

import pytest
from dotenv import load_dotenv

from nibiru import Network, Sdk
from nibiru.common import TxConfig, TxType

EXPECTED_ENV_VARS: List[str] = [
    "LCD_ENDPOINT",
    "GRPC_ENDPOINT",
    "TENDERMINT_RPC_ENDPOINT",
    "WEBSOCKET_ENDPOINT",
    "CHAIN_ID",
    "VALIDATOR_MNEMONIC",
    "ORACLE_MNEMONIC",
    "NETWORK_INSECURE",
]


def pytest_configure(config):
    load_dotenv()

    for env_var in EXPECTED_ENV_VARS:
        val = os.getenv(env_var)
        if not val:
            raise ValueError(f"Environment variable {env_var} is missing!")
        setattr(pytest, env_var, val)  # pytest.<env_var> = val

    # NETWORK_INSECURE must be a boolean
    pytest.NETWORK_INSECURE = os.getenv("NETWORK_INSECURE") != "false"


@pytest.fixture
def network() -> Network:
    return Network(
        lcd_endpoint=pytest.LCD_ENDPOINT,
        grpc_endpoint=pytest.GRPC_ENDPOINT,
        tendermint_rpc_endpoint=pytest.TENDERMINT_RPC_ENDPOINT,
        websocket_endpoint=pytest.WEBSOCKET_ENDPOINT,
        chain_id=pytest.CHAIN_ID,
        env="unit_test",
    )


@pytest.fixture
def val_node(network: Network) -> Sdk:
    tx_config = TxConfig(tx_type=TxType.BLOCK)

    return (
        Sdk.authorize(pytest.VALIDATOR_MNEMONIC)
        .with_config(tx_config)
        .with_network(network, pytest.NETWORK_INSECURE)
    )


@pytest.fixture
def agent(network: Network) -> Sdk:
    tx_config = TxConfig(tx_type=TxType.BLOCK, gas_multiplier=3)
    agent = (
        Sdk.authorize()
        .with_config(tx_config)
        .with_network(network, pytest.NETWORK_INSECURE)
    )
    return agent
