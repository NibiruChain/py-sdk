import nibiru as nib

VALIDATOR_MNEMONIC = "guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host"
tx_config = nib.TxConfig(tx_type=nib.common.TxType.BLOCK)

validator = nib.Sdk.authorize(VALIDATOR_MNEMONIC).with_config(tx_config)

validator.tx.dex.create_pool(
    creator=validator.address,
    swap_fee=0.02,
    exit_fee=0.1,
    assets=[
        nib.PoolAsset(
            token=nib.Coin(
                denom="unibi",
                amount=1000,
            ),
            weight=50,
        ),
        nib.PoolAsset(
            token=nib.Coin(
                denom="unusd",
                amount=10000,
            ),
            weight=50,
        ),
    ],
)
