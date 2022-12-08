"""
conftest.py is a special file that contains global fixture functions to be used
in tests. All test modules in the current (and child) directories can access
these fixtures.

See "Scope: sharing fixtures across classes, modules, packages or session"
- docs reference: https://docs.pytest.org/en/6.2.x/fixture.html

Fixtures available:
- sdk_val
- sdk_agent
- sdk_oracle
"""
import os
from typing import List

import pytest
from dotenv import load_dotenv

from nibiru import Network, Sdk
from nibiru.pytypes import TxConfig, TxType


def pytest_configure(config):
    load_dotenv()

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

    for env_var in EXPECTED_ENV_VARS:
        val = os.getenv(env_var)
        if not val:
            raise ValueError(f"Environment variable {env_var} is missing!")
        setattr(pytest, env_var, val)  # pytest.<env_var> = val


@pytest.fixture
def network() -> Network:
    """
    # TODO Use ping test like ts-sdk to check RPC and LCD connections
    Network(
        lcd_endpoint=pytest.LCD_ENDPOINT,
        grpc_endpoint=pytest.GRPC_ENDPOINT,
        tendermint_rpc_endpoint=pytest.TENDERMINT_RPC_ENDPOINT,
        websocket_endpoint=pytest.WEBSOCKET_ENDPOINT,
        chain_id=pytest.CHAIN_ID,
        env="unit_test",
    )
    """
    return Network.devnet(2)


TX_CONFIG: TxConfig = TxConfig(
    tx_type=TxType.BLOCK,
    gas_multiplier=1.25,
    gas_price=0.25,
)


@pytest.fixture
def sdk_val(network: Network) -> Sdk:
    tx_config = TX_CONFIG
    return (
        Sdk.authorize(pytest.VALIDATOR_MNEMONIC)
        .with_config(tx_config)
        .with_network(network)
    )


@pytest.fixture
def sdk_agent(network: Network) -> Sdk:
    tx_config = TX_CONFIG
    agent = Sdk.authorize().with_config(tx_config).with_network(network)
    return agent


# address: nibi10hj3gq54uxd9l5d6a7sn4dcvhd0l3wdgt2zvyp
@pytest.fixture
def sdk_oracle(network: Network) -> Sdk:
    tx_config = TX_CONFIG
    return (
        Sdk.authorize(pytest.ORACLE_MNEMONIC)
        .with_config(tx_config)
        .with_network(network)
    )
