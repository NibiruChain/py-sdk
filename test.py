from nibiru import Sdk, Side, PoolAsset, Composer
import time

WHALE_MNEMONIC = "guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host"


def open_position(trader):
    res = trader.tx.perp.open_position(
        sender=trader.address,
        side=Side.BUY,
        quote_asset_amount="500000000",
        leverage="5",
        base_asset_amount_limit="0",
        token_pair="axlwbtc:unusd",
    )

    print(res)


def get_position(trader):
    res = trader.query.perp.trader_position(token_pair="axlwbtc:unusd", trader=trader.address)
    print(res)


def main():
    trader = Sdk.authorize(WHALE_MNEMONIC)
    print(trader.address)

    # asyncio.get_event_loop().run_until_complete(open_position(trader))

    # time.sleep(10)
    get_position(trader)


if __name__ == "__main__":
    main()
