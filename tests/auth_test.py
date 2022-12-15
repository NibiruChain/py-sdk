import nibiru
import tests


def test_query_auth_account(sdk_val: nibiru.Sdk):
    tests.LOGGER.debug(
        "sdk_val",
    )

    query_resp: dict = sdk_val.query.auth.account(sdk_val.address)["account"]

    tests.dict_keys_must_match(query_resp, ['@type', 'address', 'pubKey', 'sequence'])


def test_query_auth_accounts(sdk_val: nibiru.Sdk):
    query_resp: dict = sdk_val.query.auth.accounts()

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
