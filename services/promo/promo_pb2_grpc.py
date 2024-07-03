# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import promo_pb2 as promo__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in promo_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class PromoServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetProductPromos = channel.unary_unary(
                '/promo.PromoService/GetProductPromos',
                request_serializer=promo__pb2.ProductPromoRequest.SerializeToString,
                response_deserializer=promo__pb2.ProductPromoResponse.FromString,
                _registered_method=True)
        self.CheckThresholdPromo = channel.unary_unary(
                '/promo.PromoService/CheckThresholdPromo',
                request_serializer=promo__pb2.ThresholdPromoRequest.SerializeToString,
                response_deserializer=promo__pb2.ThresholdPromoResponse.FromString,
                _registered_method=True)
        self.GetPromoByHash = channel.unary_unary(
                '/promo.PromoService/GetPromoByHash',
                request_serializer=promo__pb2.PromoByHashRequest.SerializeToString,
                response_deserializer=promo__pb2.PromoByHashResponse.FromString,
                _registered_method=True)


class PromoServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetProductPromos(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckThresholdPromo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPromoByHash(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PromoServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetProductPromos': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProductPromos,
                    request_deserializer=promo__pb2.ProductPromoRequest.FromString,
                    response_serializer=promo__pb2.ProductPromoResponse.SerializeToString,
            ),
            'CheckThresholdPromo': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckThresholdPromo,
                    request_deserializer=promo__pb2.ThresholdPromoRequest.FromString,
                    response_serializer=promo__pb2.ThresholdPromoResponse.SerializeToString,
            ),
            'GetPromoByHash': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPromoByHash,
                    request_deserializer=promo__pb2.PromoByHashRequest.FromString,
                    response_serializer=promo__pb2.PromoByHashResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'promo.PromoService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('promo.PromoService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class PromoService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetProductPromos(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/promo.PromoService/GetProductPromos',
            promo__pb2.ProductPromoRequest.SerializeToString,
            promo__pb2.ProductPromoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CheckThresholdPromo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/promo.PromoService/CheckThresholdPromo',
            promo__pb2.ThresholdPromoRequest.SerializeToString,
            promo__pb2.ThresholdPromoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetPromoByHash(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/promo.PromoService/GetPromoByHash',
            promo__pb2.PromoByHashRequest.SerializeToString,
            promo__pb2.PromoByHashResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
