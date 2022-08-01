Decentralized Spot Exchange (Dex)
=================================

The ``x/dex`` module is responsible for creating, joining, and
exiting liquidity pools that are dictated by an AMM for swaps.


Creation of Pool
----------------

When a pool is created, a fixed amount of 100 LP shares is minted and
sent to the pool creator. The base pool share denom is in the format of
``nibiru/pool/{poolId}`` and is displayed in the format of
``NIBIRU-POOL-{poolId}`` to the user. One ``NIBIRU-POOL-{poolId}`` token is
equivalent to 10^18 ``nibiru/pool/{poolId}`` tokens.

Pool assets are sorted in alphabetical order by default.

You can create a pool with the nibiru-py package with:

.. code:: python

    import nibiru as nib

    tx_config = nib.TxConfig(tx_type=TxType.BLOCK)
    trader = nib.Sdk.authorize(MNEMONIC).with_config(tx_config)

    trader.tx.dex.create_pool(
        creator=trader.address,
        swap_fee=0.02,
        exit_fee=0.1,
        assets=[
            nib.PoolAsset(
                token=nib.Coin(
                    denom="unibi",
                    amount=1000,
                ),
                weight=50
            ),
            nib.PoolAsset(
                token=nib.Coin(
                    denom="unusd",
                    amount=10000,
                ),
                weight=50
            ),    
        ]
    )    

You can then query the pools with the dex queries:

.. code:: python

    trader.query.dex.pools()


Joining Pool
------------

When joining a pool, users provide the tokens they are willing to
deposit. The application will try to deposit as many tokens as it can
while maintaining equal weight ratios across the pool’s assets. Usually
this means one asset acts as a limiting factor and all other tokens are
deposited in proportion to the limited token.

For example, assume there is a 50/50 pool with 100 ``tokenA`` and 100
``tokenB``. A user wishes to LP 10 ``tokenA`` and 5 ``tokenB`` into the
pool. Because ``tokenB`` is the limiting factor, all of ``tokenB`` will
be deposited and only 5 of ``tokenA`` will be deposited. The user will
be left with 5 ``tokenA`` and receive LP shares for the liquidity they
provided.

.. code:: python

    trader.tx.dex.join_pool(
        sender=trader.address,
        pool_id=4,
        tokens=[
            nib.Coin(
                denom="unibi",
                amount=10000,
            ),        
            nib.Coin(
                denom="unusd",
                amount=10000,
            )
        ]
    )

    trader.query.get_bank_balance(
        trader.address, 
        denom="nibiru/pool/4"
    )

    """
    balance {
        denom: "nibiru/pool/4"
        amount: "200000000000000000000"
    }
    """


Exiting Pool
------------

When exiting the pool, the user also provides the number of LP shares
they are returning to the pool, and will receive assets in proportion to
the LP shares returned. However, unlike joining a pool, exiting a pool
requires the user to pay the exit fee, which is set as the param of the
pool. The share of the user gets burnt.

For example, assume there is a 50/50 pool with 50 ``tokenA`` and 150
``tokenB`` and 200 total LP shares minted. A user wishes to return 20 LP
shares to the pool and withdraw their liquidity. Because 20/200 = 10%,
the user will receive 5 ``tokenA`` and 15 ``tokenB`` from the pool,
minus exit fees.

.. code:: python

    trader.tx.dex.exit_pool(
        sender=trader.address,
        pool_id=4,
        pool_shares=nib.Coin(denom="nibiru/pool/4",amount=50000000000000000000)
    )

    trader.query.get_bank_balance(trader.address, denom="nibiru/pool/4")

    """
    balance {
        denom: "nibiru/pool/4"
        amount: "150000000000000000000"
    }
    """

Swap
----

During the process of swapping a specific asset, the token user is
putting into the pool is justified as ``tokenIn``, while the token that
would be omitted after the swap is justified as ``tokenOut`` throughout
the module.

Given a tokenIn, the following calculations are done to calculate how
much tokens are to be swapped and ommitted from the pool.

-  ``tokenBalanceOut * [ 1 - { tokenBalanceIn / (tokenBalanceIn+(1-swapFee) * tokenAmountIn)}^(tokenWeightIn/tokenWeightOut)]``

The whole process is also able vice versa, the case where user provides
tokenOut. The calculation for the amount of token that the user should
be putting in is done through the following formula.

-  ``tokenBalanceIn * [{tokenBalanceOut / (tokenBalanceOut - tokenAmountOut)}^(tokenWeightOut/tokenWeightIn)-1] / tokenAmountIn``


.. code:: python

    trader.tx.dex.swap_assets(
        sender=trader.address,
        pool_id=4,
        token_in=nib.Coin(denom="unusd",amount=1000000000),
        token_out_denom="unibi"
    )

The queries in the dex query module can give estimate of the output of this command
with the current reserves of the pool:

.. code:: python

    trader.query.dex.estimate_swap_exact_amount_in(
        pool_id=4,
        token_in=nib.Coin(denom="unibi", amount=10000),
        token_out_denom="unusd"
    )


Spot Price
----------

Meanwhile, calculation of the spot price with a swap fee is done using
the following formula

-  ``spotPrice / (1-swapFee)``

where spotPrice is

-  ``(tokenBalanceIn / tokenWeightIn) / (tokenBalanceOut / tokenWeightOut)``

You can query the spot price with:

.. code:: python

    trader.query.dex.spot_price(
        pool_id=4, 
        token_in_denom="unibi", 
        token_out_denom="unusd"
    )