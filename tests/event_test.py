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
        ]

    def test_parse_attributes(self, raw_events: List[pytypes.RawEvent]):
        raw_event = raw_events[0]
        assert "attributes" in raw_event
        raw_attributes: list[dict[str, str]] = raw_event['attributes']
        attrs: dict[str, str] = pytypes.Event.parse_attributes(raw_attributes)
        assert attrs["recipient"] == "nibi1uvu52rxwqj5ndmm59y6atvx33mru9xrz6sqekr"
        assert attrs["sender"] == "nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl"
        assert attrs["amount"] == "7unibi,70unusd"

    def test_new_event(self, raw_events: List[pytypes.RawEvent]):
        event = pytypes.Event(raw_events[0])
        assert event.type == "transfer"
        for attr in ["recipient", "sender", "amount"]:
            assert attr in event.attrs
