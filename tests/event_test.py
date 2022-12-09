from typing import List

import pytest

from nibiru import pytypes


class TestEvent:
    @pytest.fixture
    def raw_events(self) -> List[pytypes.RawEvent]:
        return [
            {
                'attributes': [
                    {
                        'key': 'recipient',
                        'value': 'nibi1uvu52rxwqj5ndmm59y6atvx33mru9xrz6sqekr',
                    },
                    {
                        'key': 'sender',
                        'value': 'nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl',
                    },
                    {'key': 'amount', 'value': '7unibi,70unusd'},
                ],
                'type': 'transfer',
            },
            {
                'attributes': [
                    {'key': 'action', 'value': 'post_price'},
                    {'key': 'module', 'value': 'pricefeed'},
                    {
                        'key': 'sender',
                        'value': 'nibi10hj3gq54uxd9l5d6a7sn4dcvhd0l3wdgt2zvyp',
                    },
                ],
                'type': 'message',
            },
            {
                'attributes': [
                    {'key': 'expiry', 'value': '"2022-12-09T07:58:49.559512Z"'},
                    {
                        'key': 'oracle',
                        'value': '"nibi10hj3gq54uxd9l5d6a7sn4dcvhd0l3wdgt2zvyp"',
                    },
                    {'key': 'pair_id', 'value': '"ueth:unusd"'},
                    {'key': 'pair_price', 'value': '"1800.000000000000000000"'},
                ],
                'type': 'nibiru.pricefeed.v1.EventOracleUpdatePrice',
            },
        ]

    def test_parse_attributes(self, raw_events: List[pytypes.RawEvent]):
        raw_event = raw_events[0]
        assert "attributes" in raw_event
        raw_attributes: list[dict[str, str]] = raw_event['attributes']
        attrs: dict[str, str] = pytypes.Event.parse_attributes(raw_attributes)
        assert attrs["recipient"] == "nibi1uvu52rxwqj5ndmm59y6atvx33mru9xrz6sqekr"
        assert attrs["sender"] == "nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl"
        assert attrs["amount"] == "7unibi,70unusd"

        raw_event = raw_events[1]
        assert "attributes" in raw_event
        raw_attributes: list[dict[str, str]] = raw_event['attributes']
        attrs: dict[str, str] = pytypes.Event.parse_attributes(raw_attributes)
        assert attrs["action"] == "post_price"
        assert attrs["module"] == "pricefeed"
        oracle = "nibi10hj3gq54uxd9l5d6a7sn4dcvhd0l3wdgt2zvyp"
        assert attrs["sender"] == oracle

        raw_event = raw_events[2]
        assert "attributes" in raw_event
        raw_attributes: list[dict[str, str]] = raw_event['attributes']
        attrs: dict[str, str] = pytypes.Event.parse_attributes(raw_attributes)
        assert attrs["expiry"] == '"2022-12-09T07:58:49.559512Z"'
        assert attrs["oracle"] == f'"{oracle}"'
        assert attrs["pair_id"] == '"ueth:unusd"'
        assert attrs["pair_price"] == '"1800.000000000000000000"'

    def test_new_event(self, raw_events: List[pytypes.RawEvent]):
        event = pytypes.Event(raw_events[0])
        assert event.type == "transfer"
        for attr in ["recipient", "sender", "amount"]:
            assert attr in event.attrs

        event = pytypes.Event(raw_events[1])
        assert event.type == "message"
        for attr in ["action", "module", "sender"]:
            assert attr in event.attrs

        event = pytypes.Event(raw_events[2])
        assert event.type == "nibiru.pricefeed.v1.EventOracleUpdatePrice"
        for attr in ["expiry", "oracle", "pair_id", "pair_price"]:
            assert attr in event.attrs
