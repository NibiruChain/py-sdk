from nibiru import Composer, Sdk, Side


def test_perp_open_position(val_node: Sdk):

    # Register new trader account
    trader = Sdk.authorize()

    # Fund trader
    val_node.tx.msg_send(
        from_address=val_node.address,
        to_address=trader.address,
        coins=[
            Composer.coin(amount=1000, denom="unibi"),
            Composer.coin(amount=1000, denom="unusd"),
        ],
    )

    # Open position
    trader.tx.perp.open_position(
        sender=trader.address,
        token_pair="ubtc:unusd",
        side=Side.BUY,
        quote_asset_amount=100,
        leverage=1,
        base_asset_amount_limit=0,
        tx_type='block',
    )

    # Check position state
    res = trader.query.perp.trader_position(
        token_pair='ubtc:unusd',
        trader=trader.address,
    )

    assert res["position_notional"] == 100.0
    assert res["position"]["open_notional"] == 100.0
    assert res["unrealized_pnl"] == 0.0
    assert res["margin_ratio_index"] == 1.0
    assert res["margin_ratio_mark"] == 1.0
