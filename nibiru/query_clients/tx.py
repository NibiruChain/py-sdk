from typing import Dict, List, Union

from google.protobuf.json_format import MessageToDict
from grpc import Channel
from nibiru_proto.cosmos.tx.v1beta1 import service_pb2 as service
from nibiru_proto.cosmos.tx.v1beta1 import service_pb2_grpc as service_qrpc

from nibiru.query_clients.util import QueryClient, deserialize
from nibiru.utils import from_sdk_dec
from nibiru import pytypes

class TxQueryClient(QueryClient):
    """
    Perp allows to query the endpoints made available by the Nibiru Chain's PERP module.
    """

    def __init__(self, channel: Channel):
        self.api = service_qrpc.ServiceStub(channel)

    
    def by_hash(self, tx_hash: str) -> service.GetTxResponse:
        """ Fetches a tx by hash """
        req = service.GetTxRequest(hash=tx_hash)

        proto_output: service.GetTxResponse = self.query(
            api_callable=self.api.GetTx, req=req, should_deserialize=False
        )

        #return deserialize(proto_output)
        return proto_output
