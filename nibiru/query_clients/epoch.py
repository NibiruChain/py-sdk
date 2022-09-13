from google.protobuf.json_format import MessageToDict
from grpc import Channel
from nibiru_proto.proto.epochs import query_pb2 as epoch_type
from nibiru_proto.proto.epochs import query_pb2_grpc as epoch_query

from nibiru.query_clients.util import QueryClient


class EpochQueryClient(QueryClient):
    """
    EpochQueryClient allows to query the endpoints made available by the Nibiru Chain's epoch module.
    This module is used to time out certain events like for example funding rate payments.
    """

    def __init__(self, channel: Channel):
        self.api = epoch_query.QueryStub(channel)

    def current_epoch(self, epoch_identifier: str) -> dict:
        proto_output = self.query(
            api_callable=self.api.CurrentEpoch,
            req=epoch_type.QueryCurrentEpochRequest(identifier=epoch_identifier),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        output["currentEpoch"] = int(output["currentEpoch"])
        return output

    def epoch_infos(self) -> dict:
        proto_output = self.query(
            api_callable=self.api.EpochInfos,
            req=epoch_type.QueryEpochsInfoRequest(),
            should_deserialize=False,
        )
        output = MessageToDict(proto_output)
        return output
