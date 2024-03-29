"""
conftest.py is a special file that contains global fixture functions to be used
in tests. All test modules in the current (and child) directories can access
these fixtures.

See "Scope: sharing fixtures across classes, modules, packages or session"
- docs reference: https://docs.pytest.org/en/6.2.x/fixture.html

Fixtures available:
- client_validator
- client_new_user
"""
import os
from typing import Any, Dict, List

import dotenv
import pytest

import tests
from nibiru import ChainClient, Network, NetworkType


def pytest_configure(config):
    SetupTestConfig()


class SetupTestConfig:
    PYTEST_GLOBALS_REQUIRED: Dict[str, str] = dict(
        VALIDATOR_MNEMONIC="",
    )
    PYTEST_GLOBALS_OPTIONAL: Dict[str, Any] = dict(
        CHAIN_ID="pysdk.localnet-0",
        LCD_ENDPOINT="",
        GRPC_ENDPOINT="",
        TENDERMINT_RPC_ENDPOINT="",
        WEBSOCKET_ENDPOINT="",
    )

    PYTEST_GLOBALS: Dict[str, Any]

    def __init__(self):
        self.PYTEST_GLOBALS = {}
        dotenv.load_dotenv()
        self.set_required_globals()
        self.set_optional_globals()
        self.set_PYTEST_GLOBALS()

    def _set_pytest_global(self, name: str, value: Any):
        """Adds environment variables to the 'pytest' object and the 'PYTEST_GLOBALS'
        dictionary so that a central point of truth on what variables are set
        can be accessed from within tests.
        """
        setattr(pytest, name, value)  # pytest.<env_var> = val
        self.PYTEST_GLOBALS[name] = value

    def set_PYTEST_GLOBALS(self):
        """Combines the required and optional environment var dictionaries
        and sets the result as the value for the PYTEST_GLOBALS field.
        This is useful for inspecting the current relevant env vars in tests.
        """
        self.PYTEST_GLOBALS = {
            **self.PYTEST_GLOBALS_REQUIRED,
            **self.PYTEST_GLOBALS_OPTIONAL,
        }

    def set_required_globals(self):
        for env_var_name in self.PYTEST_GLOBALS_REQUIRED.keys():
            env_var_value = os.getenv(env_var_name)
            if not env_var_value:
                raise ValueError(f"Environment variable {env_var_name} is missing!")
            self._set_pytest_global(env_var_name, env_var_value)

    def set_optional_globals(self):
        for env_var_name in self.PYTEST_GLOBALS_OPTIONAL.keys():
            env_var_value = os.getenv(env_var_name)
            if env_var_value:
                self._set_pytest_global(env_var_name, env_var_value)


@pytest.fixture
def network() -> Network:
    return tests.fixture_network()

    # TODO test: Restore functionalty for settings the tests to run against ITN
    # or devnets for v0.21+

    # Use the chain_id to choose which Network to use
    chain_id: str = os.getenv("CHAIN_ID", "pysdk.localnet-0")
    chain_id_elements: List[str] = chain_id.split("-")
    assert len(chain_id_elements) == 3
    prefix, chain_type, chain_number = chain_id_elements
    chain_number = int(chain_number)

    chain_types: List[str] = [enum_member.value for enum_member in NetworkType]

    chain: Network
    if chain_type in chain_types:
        chain = Network.from_chain_id(chain_id=chain_id)
    else:
        chain = Network.localnet()
    return chain


@pytest.fixture
def client_validator(network: Network) -> ChainClient:
    return tests.fixture_client_validator()


@pytest.fixture
def client_new_user(network: Network) -> ChainClient:
    return tests.fixture_client_new_user()
