import nibiru
import tests


def test_module_accounts(sdk_val: nibiru.Sdk):
    module_accounts_res = sdk_val.query.util.module_accounts()
    tests.dict_keys_must_match(
        module_accounts_res,
        ["accounts"],
    )
    for account in module_accounts_res["accounts"]:
        tests.dict_keys_must_match(account, ["name", "address", "balance"])
