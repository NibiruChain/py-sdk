"""
conftest.py is a special file that contains global fixture functions to be used
in tests. All test modules in the current (and child) directories can access
these fixtures.

See "Scope: sharing fixtures across classes, modules, packages or session"
- docs reference: https://docs.pytest.org/en/6.2.x/fixture.html

Fixtures available:
- network
- val_node
"""
import os

import pytest

from nibiru import Network, Sdk
from nibiru.common import TxConfig, TxType


@pytest.fixture
def network() -> Network:
    return Network.devnet()


@pytest.fixture
def val_node(network: Network) -> Sdk:
    tx_config = TxConfig(tx_type=TxType.BLOCK)
    network_insecure: bool = True
    env_var_name = "VALIDATOR_MNEMONIC"
    val_mnemonic = os.getenv(env_var_name)
    if val_mnemonic is None:
        raise Exception(f"Missing environment variable {env_var_name}")

    return (
        Sdk.authorize(val_mnemonic)
        .with_config(tx_config)
        .with_network(network, network_insecure)
    )
