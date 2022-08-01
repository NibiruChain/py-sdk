# Copyright 2021 Nibiru Labs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Nibiru Exchange API client for Python. Example only."""

import logging

from nibiru import Sdk


def main() -> None:
    trader = Sdk.authorize(
        "guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host"
    )
    res = trader.query.perp.trader_position(
        token_pair='axlwbtc:unusd',
        trader=trader.address,
    )
    print(res)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()