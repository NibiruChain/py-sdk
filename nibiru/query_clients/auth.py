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
        proto_output = self.query(
            api_callable=self.api.Account,
            req=auth_type.QueryAccountRequest(address=address),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        return output

    def accounts(self) -> dict:
        proto_output = self.query(
            api_callable=self.api.Accounts,
            req=auth_type.QueryAccountRequest(),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        return output
