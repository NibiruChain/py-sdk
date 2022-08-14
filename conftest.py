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

    return (
        Sdk.authorize(os.getenv("VALIDATOR_MNEMONIC"))
        .with_config(tx_config)
        .with_network(network, network_insecure)
    )
