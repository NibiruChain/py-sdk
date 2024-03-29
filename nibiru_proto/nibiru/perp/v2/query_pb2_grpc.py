# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from nibiru_proto.nibiru.perp.v2 import query_pb2 as nibiru_dot_perp_dot_v2_dot_query__pb2


class QueryStub(object):
    """Query defines the gRPC querier service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.QueryPosition = channel.unary_unary(
                '/nibiru.perp.v2.Query/QueryPosition',
                request_serializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionRequest.SerializeToString,
                response_deserializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionResponse.FromString,
                )
        self.QueryPositions = channel.unary_unary(
                '/nibiru.perp.v2.Query/QueryPositions',
                request_serializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionsRequest.SerializeToString,
                response_deserializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionsResponse.FromString,
                )
        self.ModuleAccounts = channel.unary_unary(
                '/nibiru.perp.v2.Query/ModuleAccounts',
                request_serializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryModuleAccountsRequest.SerializeToString,
                response_deserializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryModuleAccountsResponse.FromString,
                )
        self.QueryMarkets = channel.unary_unary(
                '/nibiru.perp.v2.Query/QueryMarkets',
                request_serializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryMarketsRequest.SerializeToString,
                response_deserializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryMarketsResponse.FromString,
                )


class QueryServicer(object):
    """Query defines the gRPC querier service.
    """

    def QueryPosition(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryPositions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModuleAccounts(self, request, context):
        """Queries the reserve assets in a given pool, identified by a token pair.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryMarkets(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'QueryPosition': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryPosition,
                    request_deserializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionRequest.FromString,
                    response_serializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionResponse.SerializeToString,
            ),
            'QueryPositions': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryPositions,
                    request_deserializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionsRequest.FromString,
                    response_serializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionsResponse.SerializeToString,
            ),
            'ModuleAccounts': grpc.unary_unary_rpc_method_handler(
                    servicer.ModuleAccounts,
                    request_deserializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryModuleAccountsRequest.FromString,
                    response_serializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryModuleAccountsResponse.SerializeToString,
            ),
            'QueryMarkets': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryMarkets,
                    request_deserializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryMarketsRequest.FromString,
                    response_serializer=nibiru_dot_perp_dot_v2_dot_query__pb2.QueryMarketsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nibiru.perp.v2.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query defines the gRPC querier service.
    """

    @staticmethod
    def QueryPosition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nibiru.perp.v2.Query/QueryPosition',
            nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionRequest.SerializeToString,
            nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryPositions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nibiru.perp.v2.Query/QueryPositions',
            nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionsRequest.SerializeToString,
            nibiru_dot_perp_dot_v2_dot_query__pb2.QueryPositionsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModuleAccounts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nibiru.perp.v2.Query/ModuleAccounts',
            nibiru_dot_perp_dot_v2_dot_query__pb2.QueryModuleAccountsRequest.SerializeToString,
            nibiru_dot_perp_dot_v2_dot_query__pb2.QueryModuleAccountsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryMarkets(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nibiru.perp.v2.Query/QueryMarkets',
            nibiru_dot_perp_dot_v2_dot_query__pb2.QueryMarketsRequest.SerializeToString,
            nibiru_dot_perp_dot_v2_dot_query__pb2.QueryMarketsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
