import nibiru
import tests


def test_query_auth_account(val_node: nibiru.Sdk):
    query_resp: dict = val_node.query.auth.account(val_node.address)["account"]

    tests.dict_keys_must_match(
        query_resp, ['@type', 'address', 'pubKey', 'sequence', 'accountNumber']
    )


def test_query_auth_accounts(val_node: nibiru.Sdk):
    query_resp: dict = val_node.query.auth.accounts()

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
