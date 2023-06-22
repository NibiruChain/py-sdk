"""
conftest.py is a special file that contains global fixture functions to be used
in tests. All test modules in the current (and child) directories can access
these fixtures.

See "Scope: sharing fixtures across classes, modules, packages or session"
- docs reference: https://docs.pytest.org/en/6.2.x/fixture.html

Fixtures available:
- sdk_val
- sdk_agent
"""
import os
from typing import Any, Dict, List, Optional

import dotenv
import pytest

from nibiru import Network, NetworkType, Sdk
from nibiru.pytypes import TxConfig, TxType

PYTEST_GLOBALS_REQUIRED: Dict[str, str] = dict(
    VALIDATOR_MNEMONIC="",
    CHAIN_ID="nibiru-localnet-0",
)
PYTEST_GLOBALS_OPTIONAL: Dict[str, Any] = dict(
    USE_LOCALNET=False,
    LCD_ENDPOINT="",
    GRPC_ENDPOINT="",
    TENDERMINT_RPC_ENDPOINT="",
    WEBSOCKET_ENDPOINT="",
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

    # Use the chain_id to choose which Network to use
    chain_id: str = os.getenv("CHAIN_ID", "nibiru-localnet-0")
    chain_id_elements: List[str] = chain_id.split("-")
    assert len(chain_id_elements) == 3
    prefix, chain_type, chain_number = chain_id_elements
    chain_number = int(chain_number)

    chain_types: List[str] = [enum_member.value for enum_member in NetworkType]
    if chain_type in chain_types:
        return Network.from_chain_id(chain_id=chain_id)
    else:
        return Network.localnet()


@pytest.fixture
def network() -> Network:
    return get_network()


TX_CONFIG: TxConfig = TxConfig(
    tx_type=TxType.BLOCK,
    gas_multiplier=1.25,
    gas_price=0.0,
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
