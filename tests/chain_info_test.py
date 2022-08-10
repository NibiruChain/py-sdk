# chain_info_test.py
import os
import dataclasses
import pytest
import requests
import nibiru
from nibiru import common
from typing import Any, Dict, Union, List


@dataclasses.dataclass
class TestConfig:
    LCD_PORT = "1317"
    GRPC_PORT = "9090"
    VALIDATOR_MNEMONIC = os.environ["VALIDATOR_MNEMONIC"]
    CHAIN_ID = os.environ["CHAIN_ID"]
    HOST = os.environ["HOST"]


CONFIG = TestConfig()


def test_genesis_block_ping():
    """Manually query block info from the chain using a get request. This verifies that
    the configuration is valid.
    """
    host = "34.130.24.87"
    block_number = 1
    port = 26657
    url = f"http://{host}:{port}/block?height={block_number}"
    query_resp: Dict[str, Any] = requests.get(url).json()
    assert all([key in query_resp.keys() for key in ["jsonrpc", "id", "result"]])


@pytest.fixture
def network() -> nibiru.Network:
    return nibiru.Network(
        lcd_endpoint=f'http://{CONFIG.HOST}.:{CONFIG.LCD_PORT}',
        grpc_endpoint=f'{CONFIG.HOST}:{CONFIG.GRPC_PORT}',
        chain_id=CONFIG.CHAIN_ID,
        fee_denom='unibi',
        env="local",
    )


@pytest.fixture
def val_node(network: nibiru.Network) -> nibiru.Sdk:
    tx_config = nibiru.TxConfig(tx_type=common.TxType.BLOCK)
    newtork_insecure: bool = True
    return (
        nibiru.Sdk.authorize(CONFIG.VALIDATOR_MNEMONIC).with_config(tx_config).with_network(network, newtork_insecure)
    )


def test_get_chain_id(val_node: nibiru.Sdk):
    assert CONFIG.CHAIN_ID == val_node.query.get_chain_id()


def test_query_perp_params(val_node: nibiru.Sdk):
    params: Dict[str, Union[float, str]] = val_node.query.perp.params()

    perp_param_names: List[str] = [
        "ecosystemFundFeeRatio",
        "epochIdentifier",
        "feePoolFeeRatio",
        "liquidationFeeRatio",
        "partialLiquidationRatio",
        "twapLookbackWindow",
    ]
    assert all([(param_name in params) for param_name in perp_param_names])
