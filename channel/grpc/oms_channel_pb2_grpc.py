# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import oms_channel_pb2 as oms__channel__pb2

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
        + f' but the generated code in oms_channel_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class ChannelServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListBrands = channel.unary_unary(
                '/oms_channel.ChannelService/ListBrands',
                request_serializer=oms__channel__pb2.Empty.SerializeToString,
                response_deserializer=oms__channel__pb2.ListBrandsResponse.FromString,
                _registered_method=True)
        self.ListChannels = channel.unary_unary(
                '/oms_channel.ChannelService/ListChannels',
                request_serializer=oms__channel__pb2.Empty.SerializeToString,
                response_deserializer=oms__channel__pb2.ListChannelsResponse.FromString,
                _registered_method=True)
        self.ListEvents = channel.unary_unary(
                '/oms_channel.ChannelService/ListEvents',
                request_serializer=oms__channel__pb2.Empty.SerializeToString,
                response_deserializer=oms__channel__pb2.ListEventsResponse.FromString,
                _registered_method=True)
        self.GetProduct = channel.unary_unary(
                '/oms_channel.ChannelService/GetProduct',
                request_serializer=oms__channel__pb2.GetProductRequest.SerializeToString,
                response_deserializer=oms__channel__pb2.ProductResponse.FromString,
                _registered_method=True)
        self.CreateProduct = channel.unary_unary(
                '/oms_channel.ChannelService/CreateProduct',
                request_serializer=oms__channel__pb2.CreateProductRequest.SerializeToString,
                response_deserializer=oms__channel__pb2.ProductResponse.FromString,
                _registered_method=True)
        self.UpdateProduct = channel.unary_unary(
                '/oms_channel.ChannelService/UpdateProduct',
                request_serializer=oms__channel__pb2.UpdateProductRequest.SerializeToString,
                response_deserializer=oms__channel__pb2.ProductResponse.FromString,
                _registered_method=True)
        self.DeleteProduct = channel.unary_unary(
                '/oms_channel.ChannelService/DeleteProduct',
                request_serializer=oms__channel__pb2.DeleteProductRequest.SerializeToString,
                response_deserializer=oms__channel__pb2.Empty.FromString,
                _registered_method=True)
        self.ListProducts = channel.unary_unary(
                '/oms_channel.ChannelService/ListProducts',
                request_serializer=oms__channel__pb2.ListProductsRequest.SerializeToString,
                response_deserializer=oms__channel__pb2.ListProductsResponse.FromString,
                _registered_method=True)
        self.GetProductVariant = channel.unary_unary(
                '/oms_channel.ChannelService/GetProductVariant',
                request_serializer=oms__channel__pb2.GetProductVariantRequest.SerializeToString,
                response_deserializer=oms__channel__pb2.ProductVariantResponse.FromString,
                _registered_method=True)
        self.CreateProductVariant = channel.unary_unary(
                '/oms_channel.ChannelService/CreateProductVariant',
                request_serializer=oms__channel__pb2.CreateProductVariantRequest.SerializeToString,
                response_deserializer=oms__channel__pb2.ProductVariantResponse.FromString,
                _registered_method=True)
        self.UpdateProductVariant = channel.unary_unary(
                '/oms_channel.ChannelService/UpdateProductVariant',
                request_serializer=oms__channel__pb2.UpdateProductVariantRequest.SerializeToString,
                response_deserializer=oms__channel__pb2.ProductVariantResponse.FromString,
                _registered_method=True)
        self.DeleteProductVariant = channel.unary_unary(
                '/oms_channel.ChannelService/DeleteProductVariant',
                request_serializer=oms__channel__pb2.DeleteProductVariantRequest.SerializeToString,
                response_deserializer=oms__channel__pb2.Empty.FromString,
                _registered_method=True)
        self.ListProductVariants = channel.unary_unary(
                '/oms_channel.ChannelService/ListProductVariants',
                request_serializer=oms__channel__pb2.ListProductVariantsRequest.SerializeToString,
                response_deserializer=oms__channel__pb2.ListProductVariantsResponse.FromString,
                _registered_method=True)


class ChannelServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListBrands(self, request, context):
        """List all brands
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListChannels(self, request, context):
        """List all channels
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListEvents(self, request, context):
        """List all events
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProduct(self, request, context):
        """CRUD operations for products and variants
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListProducts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProductVariant(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateProductVariant(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateProductVariant(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteProductVariant(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListProductVariants(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChannelServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListBrands': grpc.unary_unary_rpc_method_handler(
                    servicer.ListBrands,
                    request_deserializer=oms__channel__pb2.Empty.FromString,
                    response_serializer=oms__channel__pb2.ListBrandsResponse.SerializeToString,
            ),
            'ListChannels': grpc.unary_unary_rpc_method_handler(
                    servicer.ListChannels,
                    request_deserializer=oms__channel__pb2.Empty.FromString,
                    response_serializer=oms__channel__pb2.ListChannelsResponse.SerializeToString,
            ),
            'ListEvents': grpc.unary_unary_rpc_method_handler(
                    servicer.ListEvents,
                    request_deserializer=oms__channel__pb2.Empty.FromString,
                    response_serializer=oms__channel__pb2.ListEventsResponse.SerializeToString,
            ),
            'GetProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProduct,
                    request_deserializer=oms__channel__pb2.GetProductRequest.FromString,
                    response_serializer=oms__channel__pb2.ProductResponse.SerializeToString,
            ),
            'CreateProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateProduct,
                    request_deserializer=oms__channel__pb2.CreateProductRequest.FromString,
                    response_serializer=oms__channel__pb2.ProductResponse.SerializeToString,
            ),
            'UpdateProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateProduct,
                    request_deserializer=oms__channel__pb2.UpdateProductRequest.FromString,
                    response_serializer=oms__channel__pb2.ProductResponse.SerializeToString,
            ),
            'DeleteProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteProduct,
                    request_deserializer=oms__channel__pb2.DeleteProductRequest.FromString,
                    response_serializer=oms__channel__pb2.Empty.SerializeToString,
            ),
            'ListProducts': grpc.unary_unary_rpc_method_handler(
                    servicer.ListProducts,
                    request_deserializer=oms__channel__pb2.ListProductsRequest.FromString,
                    response_serializer=oms__channel__pb2.ListProductsResponse.SerializeToString,
            ),
            'GetProductVariant': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProductVariant,
                    request_deserializer=oms__channel__pb2.GetProductVariantRequest.FromString,
                    response_serializer=oms__channel__pb2.ProductVariantResponse.SerializeToString,
            ),
            'CreateProductVariant': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateProductVariant,
                    request_deserializer=oms__channel__pb2.CreateProductVariantRequest.FromString,
                    response_serializer=oms__channel__pb2.ProductVariantResponse.SerializeToString,
            ),
            'UpdateProductVariant': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateProductVariant,
                    request_deserializer=oms__channel__pb2.UpdateProductVariantRequest.FromString,
                    response_serializer=oms__channel__pb2.ProductVariantResponse.SerializeToString,
            ),
            'DeleteProductVariant': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteProductVariant,
                    request_deserializer=oms__channel__pb2.DeleteProductVariantRequest.FromString,
                    response_serializer=oms__channel__pb2.Empty.SerializeToString,
            ),
            'ListProductVariants': grpc.unary_unary_rpc_method_handler(
                    servicer.ListProductVariants,
                    request_deserializer=oms__channel__pb2.ListProductVariantsRequest.FromString,
                    response_serializer=oms__channel__pb2.ListProductVariantsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'oms_channel.ChannelService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('oms_channel.ChannelService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ChannelService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListBrands(request,
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
            '/oms_channel.ChannelService/ListBrands',
            oms__channel__pb2.Empty.SerializeToString,
            oms__channel__pb2.ListBrandsResponse.FromString,
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
    def ListChannels(request,
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
            '/oms_channel.ChannelService/ListChannels',
            oms__channel__pb2.Empty.SerializeToString,
            oms__channel__pb2.ListChannelsResponse.FromString,
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
    def ListEvents(request,
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
            '/oms_channel.ChannelService/ListEvents',
            oms__channel__pb2.Empty.SerializeToString,
            oms__channel__pb2.ListEventsResponse.FromString,
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
    def GetProduct(request,
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
            '/oms_channel.ChannelService/GetProduct',
            oms__channel__pb2.GetProductRequest.SerializeToString,
            oms__channel__pb2.ProductResponse.FromString,
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
    def CreateProduct(request,
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
            '/oms_channel.ChannelService/CreateProduct',
            oms__channel__pb2.CreateProductRequest.SerializeToString,
            oms__channel__pb2.ProductResponse.FromString,
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
    def UpdateProduct(request,
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
            '/oms_channel.ChannelService/UpdateProduct',
            oms__channel__pb2.UpdateProductRequest.SerializeToString,
            oms__channel__pb2.ProductResponse.FromString,
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
    def DeleteProduct(request,
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
            '/oms_channel.ChannelService/DeleteProduct',
            oms__channel__pb2.DeleteProductRequest.SerializeToString,
            oms__channel__pb2.Empty.FromString,
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
    def ListProducts(request,
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
            '/oms_channel.ChannelService/ListProducts',
            oms__channel__pb2.ListProductsRequest.SerializeToString,
            oms__channel__pb2.ListProductsResponse.FromString,
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
    def GetProductVariant(request,
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
            '/oms_channel.ChannelService/GetProductVariant',
            oms__channel__pb2.GetProductVariantRequest.SerializeToString,
            oms__channel__pb2.ProductVariantResponse.FromString,
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
    def CreateProductVariant(request,
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
            '/oms_channel.ChannelService/CreateProductVariant',
            oms__channel__pb2.CreateProductVariantRequest.SerializeToString,
            oms__channel__pb2.ProductVariantResponse.FromString,
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
    def UpdateProductVariant(request,
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
            '/oms_channel.ChannelService/UpdateProductVariant',
            oms__channel__pb2.UpdateProductVariantRequest.SerializeToString,
            oms__channel__pb2.ProductVariantResponse.FromString,
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
    def DeleteProductVariant(request,
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
            '/oms_channel.ChannelService/DeleteProductVariant',
            oms__channel__pb2.DeleteProductVariantRequest.SerializeToString,
            oms__channel__pb2.Empty.FromString,
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
    def ListProductVariants(request,
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
            '/oms_channel.ChannelService/ListProductVariants',
            oms__channel__pb2.ListProductVariantsRequest.SerializeToString,
            oms__channel__pb2.ListProductVariantsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
