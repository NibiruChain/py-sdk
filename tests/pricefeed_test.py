# pricefeed_test.py
from datetime import datetime, timedelta
from typing import List, Optional

import pytest
from nibiru_proto.proto.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse

import nibiru
import tests
from nibiru.msg import MsgPostPrice
from tests import dict_keys_must_match, transaction_must_succeed

WHITELISTED_ORACLES: List[str] = [
    "nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl",
    "nibi15cdcxznuwpuk5hw7t678wpyesy78kwy00qcesa",
    "nibi1qqx5reauy4glpskmppy88pz25qp2py5yxvpxdt",
]


def post_price_test_tx(
    sdk: nibiru.Sdk, from_oracle: Optional[str] = None
) -> TxResponse:
    if from_oracle is None:
        from_oracle = sdk.address
    tests.LOGGER.info(f"sending 'nibid tx post price' from {from_oracle}")
    msg = MsgPostPrice(
        oracle=from_oracle,
        token0="ueth",
        token1="unusd",
        price=1800,
        expiry=datetime.utcnow() + timedelta(hours=1),
    )
    return sdk.tx.execute_msgs(msg)


def test_post_price_unwhitelisted(val_node: nibiru.Sdk):
    tests.LOGGER.info("'test_post_price_unwhitelisted' - should error")
    unwhitested_address = "nibi1pzd5e402eld9kcc3h78tmfrm5rpzlzk6hnxkvu"
    queryResp = val_node.query.pricefeed.oracles("ueth:unusd")

    assert unwhitested_address not in queryResp["oracles"]  # TODO
    tests.LOGGER.info(f"oracle address not whitelisted: {unwhitested_address}")

    with pytest.raises(
        nibiru.exceptions.SimulationError, match="unknown address"
    ) as err:
        tx_output = post_price_test_tx(sdk=val_node, from_oracle=unwhitested_address)
        err_msg = str(err)
        assert transaction_must_succeed(tx_output) is None, err_msg


def test_grpc_error(val_node: nibiru.Sdk):
    # Market ueth:unusd must be in the list of pricefeed markets
    markets_output = val_node.query.pricefeed.markets()
    assert isinstance(markets_output, dict)
    assert any(
        [market["pair_id"] == "ueth:unusd" for market in markets_output["markets"]]
    )

    # Oracle must be in the list of ueth:unusd market oracles
    ueth_unusd_market = next(
        market
        for market in markets_output["markets"]
        if market["pair_id"] == "ueth:unusd"
    )
    assert val_node.address in ueth_unusd_market["oracles"]

    # Transaction post_price in the past must raise proper error
    with pytest.raises(nibiru.exceptions.SimulationError, match="Price is expired"):
        _ = val_node.tx.execute_msgs(
            msgs=MsgPostPrice(
                val_node.address,
                token0="ueth",
                token1="unusd",
                price=1800,
                expiry=datetime.utcnow() - timedelta(hours=1),  # Price expired
            )
        )


def test_post_prices(val_node: nibiru.Sdk):

    # Market ueth:unusd must be in the list of pricefeed markets
    markets_output = val_node.query.pricefeed.markets()
    assert isinstance(markets_output, dict)
    assert any(
        [market["pair_id"] == "ueth:unusd" for market in markets_output["markets"]]
    )

    tests.LOGGER.info("Oracle must be in the list of ueth:unusd market oracles")
    ueth_unusd_market = next(
        market
        for market in markets_output["markets"]
        if market["pair_id"] == "ueth:unusd"
    )
    assert val_node.address in ueth_unusd_market["oracles"]

    tests.LOGGER.info("Transaction post_price must succeed")
    tx_output = post_price_test_tx(sdk=val_node)
    tests.LOGGER.info(
        f"nibid tx pricefeed post-price:\n{tests.format_response(tx_output)}"
    )
    transaction_must_succeed(tx_output)

    # Repeating post_price transaction.
    # Otherwise, getting "All input prices are expired" on query.pricefeed.price()
    if val_node.address not in WHITELISTED_ORACLES:
        tests.LOGGER.info(f"oracle address not whitelisted: {val_node.address}")
        with pytest.raises(Exception) as err:
            tx_output = post_price_test_tx(sdk=val_node)
            err_msg = str(err)
            assert transaction_must_succeed(tx_output) is None, err_msg
    tx_output = post_price_test_tx(sdk=val_node)
    tests.LOGGER.info(
        f"nibid tx pricefeed post-price:\n{tests.format_response(tx_output)}"
    )
    assert transaction_must_succeed(tx_output) is None

    # Raw prices must exist after post_price transaction
    raw_prices = val_node.query.pricefeed.raw_prices("ueth:unusd")["raw_prices"]
    assert len(raw_prices) >= 1

    # Raw price must be a dict with specific keys
    raw_price = raw_prices[0]
    dict_keys_must_match(raw_price, ['expiry', 'oracle_address', 'pair_id', 'price'])

    # Price feed params must be a dict with specific keys
    price_feed_params = val_node.query.pricefeed.params()["params"]
    tests.LOGGER.info(
        f"nibid query pricefeed params:\n{tests.format_response(price_feed_params)}"
    )
    dict_keys_must_match(price_feed_params, ['pairs', 'twap_lookback_window'])

    # ueth price object must be a dict with specific keys
    ueth_price = val_node.query.pricefeed.price("ueth:unusd")["price"]
    tests.LOGGER.info(
        f"nibid query pricefeed price:\n{tests.format_response(ueth_price)}"
    )
    dict_keys_must_match(ueth_price, ["pair_id", "price", "twap"])

    # At least one pair in prices must be ueth:unusd
    prices = val_node.query.pricefeed.prices()["prices"]
    tests.LOGGER.info(f"nibid query pricefeed prices:\n{tests.format_response(prices)}")
    assert any([price["pair_id"] == "ueth:unusd" for price in prices])

    # ueth price object must be a dict with specific keys
    ueth_price = next(price for price in prices if price["pair_id"] == "ueth:unusd")
    dict_keys_must_match(ueth_price, ["pair_id", "price", "twap"])
