from google.protobuf.json_format import MessageToDict
from grpc import Channel
from nibiru_proto.proto.epochs import query_pb2 as epoch_type
from nibiru_proto.proto.epochs import query_pb2_grpc as epoch_query

from nibiru.query_clients.util import QueryClient


class EpochQueryClient(QueryClient):
    """
    EpochQueryClient allows to query the endpoints made available by the epoch
    module of Nibiru Chain. This module is used to time out certain events like
    funding rate payments.
    """

    def __init__(self, channel: Channel):
        self.api = epoch_query.QueryStub(channel)

    def current_epoch(self, epoch_identifier: str) -> dict:
        """
        Returns information about the epoch specified

        Example Return Value::

        ```json
        {"current_epoch":"329"}
        ```

        Args:
            epoch_identifier(str): the identifier of the epoch, example: "week"

        Returns:

        """
        proto_output = self.query(
            api_callable=self.api.CurrentEpoch,
            req=epoch_type.QueryCurrentEpochRequest(identifier=epoch_identifier),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        output["currentEpoch"] = int(output["currentEpoch"])
        return output

    def epoch_infos(self) -> dict:
        """
        Returns all the epochs that exist and its details

        Example Return Value::

        ```json
        {
            "epochs": [
                {
                  "identifier": "15 min",
                  "start_time": "2022-12-16T22:55:34.903063726Z",
                  "duration": "900s",
                  "current_epoch": "658",
                  "current_epoch_start_time": "2022-12-23T19:10:34.903063726Z",
                  "epoch_counting_started": true,
                  "current_epoch_start_height": "427359"
                },
                {
                  "identifier": "30 min",
                  "start_time": "2022-12-16T22:55:34.903063726Z",
                  "duration": "1800s",
                  "current_epoch": "329",
                  "current_epoch_start_time": "2022-12-23T18:55:34.903063726Z",
                  "epoch_counting_started": true,
                  "current_epoch_start_height": "426741"
                }]
        }
        ```

        Returns:
            dict: the list of epochs
        """
        proto_output = self.query(
            api_callable=self.api.EpochInfos,
            req=epoch_type.QueryEpochsInfoRequest(),
            should_deserialize=False,
        )
        output = MessageToDict(proto_output)
        return output
