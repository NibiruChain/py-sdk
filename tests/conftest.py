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
from typing import Any, Dict, List, Optional

import dotenv
import pytest

from nibiru import Network, Sdk
from nibiru.pytypes import TxConfig, TxType
from tests.utils_test import can_ping, url_to_host

DEVNET_CHAIN_ID = 2

PYTEST_GLOBALS_REQUIRED: Dict[str, str] = dict(
    VALIDATOR_MNEMONIC="",
    ORACLE_MNEMONIC="",
)
PYTEST_GLOBALS_OPTIONAL: Dict[str, Any] = dict(
    use_localnet=False,
    LCD_ENDPOINT="",
    GRPC_ENDPOINT="",
    TENDERMINT_RPC_ENDPOINT="",
    WEBSOCKET_ENDPOINT="",
    CHAIN_ID="",
)
PYTEST_GLOBALS: Dict[str, Any] = {
    **PYTEST_GLOBALS_REQUIRED,  # combines dictionaries
    **PYTEST_GLOBALS_OPTIONAL,
}


def pytest_configure(config):
    dotenv.load_dotenv()

    EXPECTED_ENV_VARS: List[str] = list(PYTEST_GLOBALS.keys())

    def set_pytest_global(name: str, value: Any):
        """Adds environment variables to the 'pytest' object and the 'PYTEST_GLOBALS'
        dictionary so that a central point of truth on what variables are set
        can be accessed from within tests.
        """
        setattr(pytest, name, value)  # pytest.<env_var> = val
        PYTEST_GLOBALS[name] = value

    use_localnet: Optional[str] = os.getenv("USE_LOCALNET")
    if use_localnet is not None:
        if use_localnet.lower() == "true":
            set_pytest_global("use_localnet", True)
    if not use_localnet:
        EXPECTED_ENV_VARS = [key for key in PYTEST_GLOBALS_REQUIRED]
        set_pytest_global("use_localnet", False)

    # Set the expected environment variables. Raise a value error if one is missing
    for env_var_name in EXPECTED_ENV_VARS:
        env_var_value = os.getenv(env_var_name)
        if not env_var_value:
            raise ValueError(f"Environment variable {env_var_name} is missing!")
        set_pytest_global(env_var_name, env_var_value)


def get_network() -> Network:
    if PYTEST_GLOBALS["use_localnet"]:
        return Network.customnet()
    return Network.devnet(DEVNET_CHAIN_ID)


@pytest.fixture
def network() -> Network:
    """
    # TODO Use ping test like ts-sdk to check RPC and LCD connections
    """
    return get_network()


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    network = get_network()

    if not can_ping("www.google.com"):
        raise TimeoutError(f"Cannot ping google.com")

    if not can_ping(url_to_host(network.lcd_endpoint)):
        raise TimeoutError(
            f"Lcd Endpoint {url_to_host(network.lcd_endpoint)} timed out"
        )

    if not can_ping(url_to_host(network.grpc_endpoint)):
        raise TimeoutError(
            f"Grpc Endpoint {url_to_host(network.grpc_endpoint)} timed out"
        )

    if not can_ping(url_to_host(network.tendermint_rpc_endpoint)):
        raise TimeoutError(
            f"Tendermint Rpc Endpoint {url_to_host(network.tendermint_rpc_endpoint)} timed out"
        )


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
