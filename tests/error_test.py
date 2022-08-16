# error_test.py
from datetime import datetime, timedelta

from pytest import raises

import nibiru


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
    with raises(nibiru.exceptions.TxError, match="Price is expired"):
        oracle_agent.tx.pricefeed.post_price(
            oracle_agent.address,
            token0="unibi",
            token1="unusd",
            price=10,
            expiry=datetime.utcnow() - timedelta(hours=1),
        )
