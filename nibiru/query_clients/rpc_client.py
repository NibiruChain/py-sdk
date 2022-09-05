"""
The ChainQueryClient client is used to create RPC requests to a node and get information about the chain.
We prefer to use GRPC (with protobuf serialization) for all interactions with the chain, but some requests
such as current block or the version of the chain are only available through RPC requests.
"""

import json
from typing import Dict, List, Union

import requests
import requests.exceptions


class ChainQueryClient:
    rpc_endpoint: str

    def __init__(self, rpc_endpoint: str):
        assert rpc_endpoint != "", "No RPC endpoint provided"
        self.rpc_endpoint = rpc_endpoint
        self.timeout = 1000

    def rpc_get(self, endpoint: str) -> Union[List, Dict]:
        """
        Request payload from the RPC endpoint at the specified endpoint.

        Args:
            endpoint (str): The path to the endpoint to fetch.

        Returns:
            dict: The output of the query
        """
        return json.loads(
            requests.get(
                self.rpc_endpoint + "/" + endpoint, timeout=self.timeout
            ).content
        )

    def version(self) -> str:
        """
        Retrieve the current version that the chain is running on the node queried.
        """
        version = self.rpc_get("abci_info?")["result"]["response"]["version"]
        if version[0] != "v":
            version = "v" + version

        return version

    def last_block_height(self) -> int:
        """
        Retrieve the last block height of the chain.
        """
        return int(
            self.rpc_get("abci_info?")["result"]["response"]["last_block_height"]
        )
