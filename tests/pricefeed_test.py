# pricefeed_test.py
from datetime import datetime, timedelta
from typing import List, Optional

import pytest
from nibiru_proto.proto.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse

import nibiru
import tests
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
    return sdk.tx.pricefeed.post_price(
        from_oracle,
        token0="unibi",
        token1="unusd",
        price=10,
        expiry=datetime.utcnow() + timedelta(hours=1),
    )


def test_post_price_unwhitelisted(agent: nibiru.Sdk):
    tests.LOGGER.info("'test_post_price_unwhitelisted' - should error")
    unwhitested_address = "nibi1pzd5e402eld9kcc3h78tmfrm5rpzlzk6hnxkvu"
    queryResp = agent.query.pricefeed.oracles("unibi:unusd")

    assert unwhitested_address not in queryResp["oracles"]  # TODO
    tests.LOGGER.info(f"oracle address not whitelisted: {unwhitested_address}")

    with pytest.raises(
        nibiru.exceptions.TxError, match="Oracle does not exist or not authorized"
    ) as err:
        tx_output = post_price_test_tx(sdk=agent, from_oracle=unwhitested_address)
        err_msg = str(err)
        assert transaction_must_succeed(tx_output) is None, err_msg


def test_grpc_error(oracle_agent):
    # Market unibi:unusd must be in the list of pricefeed markets
    markets_output = oracle_agent.query.pricefeed.markets()
    assert isinstance(markets_output, dict)
    assert any(
        [market["pair_id"] == "unibi:unusd" for market in markets_output["markets"]]
    )

    # Oracle must be in the list of unibi:unusd market oracles
    unibi_unusd_market = next(
        market
        for market in markets_output["markets"]
        if market["pair_id"] == "unibi:unusd"
    )
    assert oracle_agent.address in unibi_unusd_market["oracles"]

    # Transaction post_price in the past must raise proper error
    with pytest.raises(nibiru.exceptions.TxError, match="Price is expired"):
        oracle_agent.tx.pricefeed.post_price(
            oracle_agent.address,
            token0="unibi",
            token1="unusd",
            price=10,
            expiry=datetime.utcnow() - timedelta(hours=1),  # Price expired
        )


def test_post_prices(oracle_agent: nibiru.Sdk):

    # Market unibi:unusd must be in the list of pricefeed markets
    markets_output = oracle_agent.query.pricefeed.markets()
    assert isinstance(markets_output, dict)
    assert any(
        [market["pair_id"] == "unibi:unusd" for market in markets_output["markets"]]
    )

    tests.LOGGER.info("Oracle must be in the list of unibi:unusd market oracles")
    unibi_unusd_market = next(
        market
        for market in markets_output["markets"]
        if market["pair_id"] == "unibi:unusd"
    )
    assert oracle_agent.address in unibi_unusd_market["oracles"]

    tests.LOGGER.info("Transaction post_price must succeed")
    tx_output = post_price_test_tx(sdk=oracle_agent)
    transaction_must_succeed(tx_output)

    # Repeating post_price transaction.
    # Otherwise, getting "All input prices are expired" on query.pricefeed.price()
    if oracle_agent.address not in WHITELISTED_ORACLES:
        tests.LOGGER.info(f"oracle address not whitelisted: {oracle_agent.address}")
        with pytest.raises(Exception) as err:
            tx_output = post_price_test_tx(sdk=oracle_agent)
            err_msg = str(err)
            assert transaction_must_succeed(tx_output) is None, err_msg
    tx_output = post_price_test_tx(sdk=oracle_agent)
    assert transaction_must_succeed(tx_output) is None

    # Raw prices must exist after post_price transaction
    raw_prices = oracle_agent.query.pricefeed.raw_prices("unibi:unusd")["raw_prices"]
    assert len(raw_prices) >= 1

    # Raw price must be a dict with specific keys
    raw_price = raw_prices[0]
    dict_keys_must_match(raw_price, ['expiry', 'oracle_address', 'pair_id', 'price'])

    # Price feed params must be a dict with specific keys
    price_feed_params = oracle_agent.query.pricefeed.params()["params"]
    dict_keys_must_match(price_feed_params, ['pairs', 'twap_lookback_window'])

    # Unibi price object must be a dict with specific keys
    unibi_price = oracle_agent.query.pricefeed.price("unibi:unusd")["price"]
    dict_keys_must_match(unibi_price, ["pair_id", "price"])

    # At least one pair in prices must be unibi:unusd
    prices = oracle_agent.query.pricefeed.prices()["prices"]
    assert any([price["pair_id"] == "unibi:unusd" for price in prices])

    # Unibi price object must be a dict with specific keys
    unibi_price = next(price for price in prices if price["pair_id"] == "unibi:unusd")
    dict_keys_must_match(unibi_price, ["pair_id", "price"])
