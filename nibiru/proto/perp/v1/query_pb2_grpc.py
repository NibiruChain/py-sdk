# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from perp.v1 import query_pb2 as perp_dot_v1_dot_query__pb2


class QueryStub(object):
    """Query defines the gRPC querier service."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Params = channel.unary_unary(
            '/nibiru.perp.v1.Query/Params',
            request_serializer=perp_dot_v1_dot_query__pb2.QueryParamsRequest.SerializeToString,
            response_deserializer=perp_dot_v1_dot_query__pb2.QueryParamsResponse.FromString,
        )
        self.QueryTraderPosition = channel.unary_unary(
            '/nibiru.perp.v1.Query/QueryTraderPosition',
            request_serializer=perp_dot_v1_dot_query__pb2.QueryTraderPositionRequest.SerializeToString,
            response_deserializer=perp_dot_v1_dot_query__pb2.QueryTraderPositionResponse.FromString,
        )


class QueryServicer(object):
    """Query defines the gRPC querier service."""

    def Params(self, request, context):
        """Parameters queries the parameters of the x/perp module."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryTraderPosition(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Params': grpc.unary_unary_rpc_method_handler(
            servicer.Params,
            request_deserializer=perp_dot_v1_dot_query__pb2.QueryParamsRequest.FromString,
            response_serializer=perp_dot_v1_dot_query__pb2.QueryParamsResponse.SerializeToString,
        ),
        'QueryTraderPosition': grpc.unary_unary_rpc_method_handler(
            servicer.QueryTraderPosition,
            request_deserializer=perp_dot_v1_dot_query__pb2.QueryTraderPositionRequest.FromString,
            response_serializer=perp_dot_v1_dot_query__pb2.QueryTraderPositionResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler('nibiru.perp.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query defines the gRPC querier service."""

    @staticmethod
    def Params(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/nibiru.perp.v1.Query/Params',
            perp_dot_v1_dot_query__pb2.QueryParamsRequest.SerializeToString,
            perp_dot_v1_dot_query__pb2.QueryParamsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def QueryTraderPosition(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/nibiru.perp.v1.Query/QueryTraderPosition',
            perp_dot_v1_dot_query__pb2.QueryTraderPositionRequest.SerializeToString,
            perp_dot_v1_dot_query__pb2.QueryTraderPositionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
