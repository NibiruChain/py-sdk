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
from typing import Dict

import dotenv
import pytest

from nibiru import Network, Sdk
from nibiru.pytypes import TxConfig, TxType

PYTEST_GLOBALS: Dict[str, str] = dict(
    VALIDATOR_MNEMONIC="",
)


def pytest_configure():
    dotenv.load_dotenv()

    # Set the expected environment variables. Raise a value error if one is missing
    for env_var_name in PYTEST_GLOBALS.keys():
        env_var_value = os.getenv(env_var_name)
        if not env_var_value:
            raise ValueError(f"Environment variable {env_var_name} is missing!")
        setattr(pytest, env_var_name, env_var_value)
        PYTEST_GLOBALS[env_var_name] = env_var_value


@pytest.fixture
def network() -> Network:
    return Network.customnet()


@pytest.fixture
def sdk_val(network: Network) -> Sdk:
    return (
        Sdk.authorize(pytest.VALIDATOR_MNEMONIC)
        .with_config(
            TxConfig(
                tx_type=TxType.BLOCK,
                gas_multiplier=1.25,
                gas_price=0.25,
            )
        )
        .with_network(network)
    )


@pytest.fixture
def sdk_agent(network: Network) -> Sdk:
    agent = (
        Sdk.authorize()
        .with_config(
            TxConfig(
                tx_type=TxType.BLOCK,
                gas_multiplier=1.25,
                gas_price=0.25,
            )
        )
        .with_network(network)
    )
    return agent
