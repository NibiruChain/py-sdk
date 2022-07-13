# Copyright 2022 Nibiru Chain
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


import logging

from nibiru import Sdk, Composer, PoolAsset


def main() -> None:
    trader = Sdk.authorize(
        "guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host"
    )
    res = trader.tx.dex.create_pool(
        creator=trader.address,
        swap_fee="2",
        exit_fee="3",
        assets=[
            PoolAsset(token=Composer.coin(4, "unusd"), weight="3"),
            PoolAsset(token=Composer.coin(5, "unibi"), weight="4"),
        ],
    )
    print(res)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
