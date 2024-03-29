# stories_test.py

import pytest

import nibiru
import tests


@pytest.mark.order(-2)
def test_query_tx_by_hash():
    """Tests runs that broadcast transactions build a collection of
    'BroadcastTxResp' objects that may each hold a tx hash. Each successful
    broadcast should have a hash and be queriable.
    """
    sdk = tests.fixture_client_validator()
    story: tests.FullTxStory
    for idx, story in enumerate(tests.FULL_TX_STORIES):
        if story.broadcast_resp.code == 0:
            tx_hash = story.broadcast_resp.tx_hash
            assert isinstance(tx_hash, str)
            check_tx_by_hash(sdk=sdk, tx_hash=tx_hash, idx=idx)


def check_tx_by_hash(sdk: nibiru.ChainClient, tx_hash: str, idx: int):
    try:
        query_tx_resp = sdk.tx.client.tx_by_hash(tx_hash=tx_hash)
        tests.FULL_TX_STORIES[idx].query_tx_resp = query_tx_resp
    except BaseException as err:
        tests.raises(ok_errs=["InactiveRpcError", "tx not found"], err=err)


@pytest.mark.order(after="test_query_tx_by_hash")
def test_parse_tx_resp():
    for _, story in enumerate(tests.FULL_TX_STORIES):
        if story.query_tx_resp is not None:
            assert isinstance(story.query_tx_resp, dict)
            tests.dict_keys_must_match(story.query_tx_resp, ["tx", "tx_response"])

            tx_resp = story.query_tx_resp.get("tx_response")
            assert isinstance(tx_resp, dict)
            tests.dict_keys_must_match(
                tx_resp,
                keys=(
                    [
                        'height',
                        'txhash',
                        'codespace',
                        'code',
                        'data',
                        'raw_log',
                        'logs',
                        'info',
                    ]
                    + ['gas_wanted', 'gas_used', 'tx', 'timestamp', 'events']
                ),
            )
