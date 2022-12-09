# pricefeed_test.py
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pytest
from nibiru_proto.proto.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse

import nibiru
import tests
from nibiru.msg import MsgPostPrice
from tests import dict_keys_must_match, transaction_must_succeed

WHITELISTED_ORACLES: Dict[str, str] = {
    "nibi1hk04vteklhmtwe0zpt7023p5zcgu49e5v3atyp": "CoinGecko oracle",
    "nibi10hj3gq54uxd9l5d6a7sn4dcvhd0l3wdgt2zvyp": "CoinMarketCap oracle",
    "nibi1r8gjajmlp9tkff0759rmujv568pa7q6v7u4m3z": "Binance oracle",
}


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


def test_post_price_unwhitelisted(sdk_oracle: nibiru.Sdk):
    tests.LOGGER.info("'test_post_price_unwhitelisted' - should error")
    unwhitested_address = "nibi1pzd5e402eld9kcc3h78tmfrm5rpzlzk6hnxkvu"
    queryResp = sdk_oracle.query.pricefeed.oracles("ueth:unusd")

    assert unwhitested_address not in queryResp["oracles"]  # TODO
    tests.LOGGER.info(f"oracle address not whitelisted: {unwhitested_address}")

    with pytest.raises(
        nibiru.exceptions.SimulationError, match="unknown address"
    ) as err:
        tx_output = post_price_test_tx(sdk=sdk_oracle, from_oracle=unwhitested_address)
        err_msg = str(err)
        assert transaction_must_succeed(tx_output) is None, err_msg


def test_grpc_error(sdk_oracle: nibiru.Sdk):
    # Market ueth:unusd must be in the list of pricefeed markets
    markets_output = sdk_oracle.query.pricefeed.markets()
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
    assert sdk_oracle.address in ueth_unusd_market["oracles"]

    # Transaction post_price in the past must raise proper error
    with pytest.raises(nibiru.exceptions.SimulationError, match="Price is expired"):
        _ = sdk_oracle.tx.execute_msgs(
            msgs=MsgPostPrice(
                sdk_oracle.address,
                token0="ueth",
                token1="unusd",
                price=1800,
                expiry=datetime.utcnow() - timedelta(hours=1),  # Price expired
            )
        )


@pytest.mark.order(2)
def test_post_prices(sdk_oracle: nibiru.Sdk):

    # Market ueth:unusd must be in the list of pricefeed markets
    markets_output = sdk_oracle.query.pricefeed.markets()
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
    assert sdk_oracle.address in ueth_unusd_market["oracles"]

    tests.LOGGER.info("Transaction post_price must succeed")
    tx_output = post_price_test_tx(sdk=sdk_oracle)
    tests.LOGGER.info(
        f"nibid tx pricefeed post-price:\n{tests.format_response(tx_output)}"
    )
    transaction_must_succeed(tx_output)

    # Repeating post_price transaction.
    # Otherwise, getting "All input prices are expired" on query.pricefeed.price()
    if sdk_oracle.address not in WHITELISTED_ORACLES.keys():
        tests.LOGGER.info(f"oracle address not whitelisted: {sdk_oracle.address}")
        with pytest.raises(Exception) as err:
            tx_output = post_price_test_tx(sdk=sdk_oracle)
            err_msg = str(err)
            assert transaction_must_succeed(tx_output) is None, err_msg
    tx_output = post_price_test_tx(sdk=sdk_oracle)
    tests.LOGGER.info(
        f"nibid tx pricefeed post-price:\n{tests.format_response(tx_output)}"
    )
    assert transaction_must_succeed(tx_output) is None
    sdk_oracle.query.wait_for_next_block()


@pytest.mark.order(3)
def test_pricefeed_queries(sdk_oracle: nibiru.Sdk):

    # Raw prices must exist after post_price transaction
    raw_prices: List[dict] = sdk_oracle.query.pricefeed.raw_prices("ueth:unusd")[
        "raw_prices"
    ]
    assert len(raw_prices) >= 1

    # Raw price must be a dict with specific keys
    raw_price = raw_prices[0]
    dict_keys_must_match(raw_price, ['expiry', 'oracle_address', 'pair_id', 'price'])

    # Price feed params must be a dict with specific keys
    price_feed_params = sdk_oracle.query.pricefeed.params()["params"]
    tests.LOGGER.info(
        f"nibid query pricefeed params:\n{tests.format_response(price_feed_params)}"
    )
    dict_keys_must_match(price_feed_params, ['pairs', 'twap_lookback_window'])

    # ueth price object must be a dict with specific keys
    ueth_price = sdk_oracle.query.pricefeed.price("ueth:unusd")["price"]
    tests.LOGGER.info(
        f"nibid query pricefeed price:\n{tests.format_response(ueth_price)}"
    )
    dict_keys_must_match(ueth_price, ["pair_id", "price", "twap"])

    # At least one pair in prices must be ueth:unusd
    prices = sdk_oracle.query.pricefeed.prices()["prices"]
    tests.LOGGER.info(f"nibid query pricefeed prices:\n{tests.format_response(prices)}")
    assert any([price["pair_id"] == "ueth:unusd" for price in prices])

    # ueth price object must be a dict with specific keys
    ueth_price = next(price for price in prices if price["pair_id"] == "ueth:unusd")
    dict_keys_must_match(ueth_price, ["pair_id", "price", "twap"])
