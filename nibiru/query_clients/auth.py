from google.protobuf.json_format import MessageToDict
from grpc import Channel
from nibiru_proto.proto.cosmos.auth.v1beta1 import query_pb2 as auth_type
from nibiru_proto.proto.cosmos.auth.v1beta1 import query_pb2_grpc as auth_query

from nibiru.query_clients.util import QueryClient


class AuthQueryClient(QueryClient):
    """
    AuthQueryClient allows to query the endpoints made available by the Nibiru Chain's auth module.
    """

    def __init__(self, channel: Channel):
        self.api = auth_query.QueryStub(channel)

    def account(self, address: str) -> dict:
        """
        Returns information of the given account

        Example Return Value::

        ```json
        {
          "address": "nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl",
          "pub_key": null,
          "account_number": "17",
          "sequence": "0"
        }
        ```

        Args:
            address(str): the address of the account we want to get information

        Returns:
            dict: a dictionary containing information of the account

        """
        proto_output = self.query(
            api_callable=self.api.Account,
            req=auth_type.QueryAccountRequest(address=address),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        return output

    def accounts(self) -> dict:
        """
        Accounts returns all the existing accounts

        Example Return Value::

        ```json
        {
        "accounts": [
            {
              "address": "nibi1qqrg9ntgkavhxyn3zq0zmz85yp8vxgd9gm85pp",
              "pub_key": null,
              "account_number": "16246",
              "sequence": "0"
            },
            {
              "address": "nibi1qqrhxfwt6eu66v6mcdt7zc6xhqnw0w54u3rep3",
              "pub_key": null,
              "account_number": "6927",
              "sequence": "0"
            }
          ]
        }
        ```

        Returns:
            dict: a dictionary with information of all the existing accounts paginated

        """
        proto_output = self.query(
            api_callable=self.api.Accounts,
            req=auth_type.QueryAccountRequest(),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        return output
