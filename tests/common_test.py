from typing import List

import pytest

from nibiru import common


class TestEvent:
    @pytest.fixture
    def raw_events(self) -> List[common.RawEvent]:
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
            }
        ]

    def test_parse_attributes(self, raw_events: List[common.RawEvent]):
        assert "attributes" in raw_events[0]
        raw_attributes: list[dict[str, str]] = raw_events[0]['attributes']

        attrs: dict[str, str] = common.Event.parse_attributes(raw_attributes)

        assert attrs["recipient"] == "nibi1uvu52rxwqj5ndmm59y6atvx33mru9xrz6sqekr"
        assert attrs["sender"] == "nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl"
        assert attrs["amount"] == "7unibi,70unusd"
