# pricefeed_test.py
from datetime import datetime, timedelta

from tests import dict_keys_must_match, transaction_must_succeed


class TestPricefeed:
    def test_post_prices(self, oracle_agent):

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

        # Transaction post_price must succeed
        tx_output = oracle_agent.tx.pricefeed.post_price(
            oracle_agent.address,
            token0="unibi",
            token1="unusd",
            price=10,
            expiry=datetime.utcnow() + timedelta(hours=1),
        )
        transaction_must_succeed(tx_output)

        # Repeating post_price transaction.
        # Otherwise, getting "All input prices are expired" on query.pricefeed.price()
        tx_output = oracle_agent.tx.pricefeed.post_price(
            oracle_agent.address,
            token0="unibi",
            token1="unusd",
            price=10,
            expiry=datetime.utcnow() + timedelta(hours=1),
        )
        transaction_must_succeed(tx_output)

        # Raw prices must exist after post_price transaction
        raw_prices = oracle_agent.query.pricefeed.raw_prices("unibi:unusd")[
            "raw_prices"
        ]
        assert len(raw_prices) >= 1

        # Raw price must be a dict with specific keys
        raw_price = raw_prices[0]
        dict_keys_must_match(
            raw_price, ['expiry', 'oracle_address', 'pair_id', 'price']
        )

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
        unibi_price = next(
            price for price in prices if price["pair_id"] == "unibi:unusd"
        )
        dict_keys_must_match(unibi_price, ["pair_id", "price"])
