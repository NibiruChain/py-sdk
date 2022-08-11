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

from nibiru import Composer, Sdk


def main() -> None:
    sender = Sdk.authorize(
        "guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host"
    )
    receiver = Sdk.authorize()

    res = sender.tx_client.msg_send(
        from_address=sender.address,
        to_address=receiver.address,
        coins=[
            Composer.coin(amount=5, denom="unibi"),
            Composer.coin(amount=3, denom="unusd"),
        ],
        # additional params for gas price can be passed
        # gas_price = 7,
        # gas_multiplier = 1.25,
        # gas_wanted = 50_000,
    )
    logging.info("Result: %s", res)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
