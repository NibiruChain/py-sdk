import nibiru
import tests


def test_query_current_epoch(sdk_val: nibiru.Sdk):
    query_resp: dict = sdk_val.query.epoch.current_epoch("15 min")
    assert query_resp["currentEpoch"] > 0


def test_query_epoch_info(sdk_val: nibiru.Sdk):
    query_resp: dict = sdk_val.query.epoch.epoch_infos()
    assert len(query_resp["epochs"]) > 0

    for epoch in query_resp["epochs"]:
        tests.dict_keys_must_match(
            epoch,
            [
                "identifier",
                "startTime",
                "duration",
                "currentEpoch",
                "currentEpochStartTime",
                "epochCountingStarted",
                "currentEpochStartHeight",
            ],
        )
