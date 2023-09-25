from nibiru import ChainClient


def test_query_auth_account(client_validator: ChainClient):
    _: dict = client_validator.query.auth.account(client_validator.address)["account"]


def test_query_auth_accounts(client_validator):
    query_resp: dict = client_validator.query.auth.accounts()

    for account in query_resp["accounts"]:
        assert all(
            [
                key
                in [
                    '@type',
                    'address',
                    'pubKey',
                    'accountNumber',
                    'sequence',
                    'baseAccount',
                    'name',
                    'permissions',
                ]
                for key in account.keys()
            ]
        )
