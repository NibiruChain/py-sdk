Module nibiru.query_clients.dex
===============================

Classes
-------

`DexQueryClient(channel: grpc.Channel)`
:   Dex allows to query the endpoints made available by the Nibiru Chain's DEX module.

    ### Ancestors (in MRO)

    * nibiru.query_clients.util.QueryClient

    ### Methods

    `estimate_exit_exact_amount_in(self, pool_id: int, num_shares: int) ‑> dict`
    :   Estimate the output of an exit pool transaction with the current level of reserves

        Example Return Value::

            {
                "tokensOut": [
                    {
                        "denom": "unibi",
                        "amount": 1000.5
                    },
                    {
                        "denom": "unusd",
                        "amount": 100.2
                    }
                ]
            }

        Args:
            pool_id (int): The id of the pool to query
            num_shares (int): The number of shares to provide

        Returns:
            dict: The output of the query

    `estimate_join_exact_amount_in(self, pool_id: int, tokens_ins: List[nibiru.pytypes.common.Coin]) ‑> dict`
    :   Estimate the number of share given for a join pool operation

        Example Return Value::

            {
                "poolSharesOut": 100000000000000.0,
                "remCoins": [
                    {
                        "denom": "unibi",
                        "amount": 0.999
                    }
                ]
            }

        Args:
            pool_id (int): The id of the pool to query
            tokens_ins (List[Coin]): The amount of tokens provided

        Returns:
            dict: The output of the query

    `estimate_swap_exact_amount_in(self, pool_id: int, token_in: nibiru.pytypes.common.Coin, token_out_denom: str) ‑> dict`
    :   Estimate the output of the swap with the current reserves

        Example Return Value::

            {
                "tokenOut": {
                    "denom": "unusd",
                    "amount": 0.004948999999999999
                }
            }

        Args:
            pool_id (int): The pool id to query
            token_in (Coin): The amount of tokens to provide
            token_out_denom (str): The denomination of the token out

        Returns:
            dict: The output of the query

    `params(self) ‑> dict`
    :   Requests the parameters of the dex module.

        Example Return Value::

            {
                "startingPoolNumber": "1",
                "poolCreationFee": [
                    {
                        "denom": "unibi",
                        "amount": 1000.0
                    }
                ],
                "whitelistedAsset": [
                    "unibi",
                    "uusdc",
                    "unusd",
                    "stake"
                ]
            }

        Returns:
            dict: The parameters fo the dex module.

    `pools(self, **kwargs)`
    :   Return all available pools in the dex module.

        Example Return Value::

            [
                {
                    "id": "1",
                    "address": "nibi1w00c7pqkr5z7ptewg5z87j2ncvxd88w43ug679",
                    "poolParams": {
                        "swapFee": 0.02,
                        "exitFee": 0.1
                    },
                    "poolAssets": [
                        {
                            "token": {
                                "denom": "unibi",
                                "amount": 0.001
                            },
                            "weight": "53687091200000000"
                        },
                        {
                            "token": {
                                "denom": "unusd",
                                "amount": 0.01
                            },
                            "weight": "53687091200000000"
                        }
                    ],
                    "totalWeight": "107374182400000000",
                    "totalShares": {
                        "denom": "nibiru/pool/1",
                        "amount": 100000000000000.0
                    }
                }
            ]


        Args:
            key (bytes): The page key for the next page. Only key or offset should be set
            offset (int): The number of entries to skip. Only offset or key should be set
            limit (int): The number of max results in the page
            count_total (bool): Indicates if the response should contain the total number of results
            reverse (bool): Indicates if the results should be returned in descending order

        Returns:
            dict: The output of the query

    `spot_price(self, pool_id: int, token_in_denom: str, token_out_denom: str) ‑> dict`
    :   Returns the spot price of the pool using token in as base and token out as quote

        Args:
            pool_id (int): _description_
            token_in_denom (str): _description_
            token_out_denom (str): _description_

        Returns:
            dict: _description_

    `total_liquidity(self) ‑> dict`
    :   Returns the total amount of liquidity for the dex module

        Example Return Value::

            {
                "liquidity": [
                    {
                        "denom": "unibi",
                        "amount": 0.001
                    },
                    {
                        "denom": "unusd",
                        "amount": 0.01
                    }
                ]
            }

        Returns:
            dict: The total liquidity of the protocol

    `total_pool_liquidity(self, pool_id: int) ‑> dict`
    :   Returns the total liquidity for a specific pool id

        Example Return Value::

            {
                "liquidity": [
                    {
                        "denom": "unibi",
                        "amount": 0.001
                    },
                    {
                        "denom": "unusd",
                        "amount": 0.01
                    }
                ]
            }

        Args:
            pool_id (int): the id of the pool

        Returns:
            dict: The total liquidity for the pool

    `total_shares(self, pool_id: int) ‑> dict`
    :   Returns the total amount of shares for the pool specified

        Example Return Value::

            {
                "totalShares": {
                    "denom": "nibiru/pool/1",
                    "amount": 100000000000000.0
                }
            }

        Args:
            pool_id (int): The id of the pool

        Returns:
            dict: The amount of shares for the pool
