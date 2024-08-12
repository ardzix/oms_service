# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import cart_pb2 as cart__pb2

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
        + f' but the generated code in cart_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class CartServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetOrCreateCart = channel.unary_unary(
                '/cart.CartService/GetOrCreateCart',
                request_serializer=cart__pb2.GetOrCreateCartRequest.SerializeToString,
                response_deserializer=cart__pb2.GetOrCreateCartResponse.FromString,
                _registered_method=True)
        self.GetCartDetail = channel.unary_unary(
                '/cart.CartService/GetCartDetail',
                request_serializer=cart__pb2.GetCartDetailRequest.SerializeToString,
                response_deserializer=cart__pb2.GetCartDetailResponse.FromString,
                _registered_method=True)
        self.AddToCart = channel.unary_unary(
                '/cart.CartService/AddToCart',
                request_serializer=cart__pb2.AddToCartRequest.SerializeToString,
                response_deserializer=cart__pb2.GetCartItemDetailResponse.FromString,
                _registered_method=True)
        self.ApplyCartItemPromo = channel.unary_unary(
                '/cart.CartService/ApplyCartItemPromo',
                request_serializer=cart__pb2.ApplyCartItemPromoRequest.SerializeToString,
                response_deserializer=cart__pb2.GetCartItemDetailResponse.FromString,
                _registered_method=True)
        self.RemoveCartItem = channel.unary_unary(
                '/cart.CartService/RemoveCartItem',
                request_serializer=cart__pb2.RemoveCartItemRequest.SerializeToString,
                response_deserializer=cart__pb2.RemoveCartItemResponse.FromString,
                _registered_method=True)
        self.ClearCart = channel.unary_unary(
                '/cart.CartService/ClearCart',
                request_serializer=cart__pb2.ClearCartRequest.SerializeToString,
                response_deserializer=cart__pb2.ClearCartResponse.FromString,
                _registered_method=True)


class CartServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetOrCreateCart(self, request, context):
        """Get or create a cart by user_hash and brand_hash
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCartDetail(self, request, context):
        """Get cart details by cart hash
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddToCart(self, request, context):
        """Add an item to the cart
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ApplyCartItemPromo(self, request, context):
        """Apply promo to a cart item
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveCartItem(self, request, context):
        """Remove an item from the cart
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClearCart(self, request, context):
        """Clear all items from the cart
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CartServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetOrCreateCart': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrCreateCart,
                    request_deserializer=cart__pb2.GetOrCreateCartRequest.FromString,
                    response_serializer=cart__pb2.GetOrCreateCartResponse.SerializeToString,
            ),
            'GetCartDetail': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCartDetail,
                    request_deserializer=cart__pb2.GetCartDetailRequest.FromString,
                    response_serializer=cart__pb2.GetCartDetailResponse.SerializeToString,
            ),
            'AddToCart': grpc.unary_unary_rpc_method_handler(
                    servicer.AddToCart,
                    request_deserializer=cart__pb2.AddToCartRequest.FromString,
                    response_serializer=cart__pb2.GetCartItemDetailResponse.SerializeToString,
            ),
            'ApplyCartItemPromo': grpc.unary_unary_rpc_method_handler(
                    servicer.ApplyCartItemPromo,
                    request_deserializer=cart__pb2.ApplyCartItemPromoRequest.FromString,
                    response_serializer=cart__pb2.GetCartItemDetailResponse.SerializeToString,
            ),
            'RemoveCartItem': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveCartItem,
                    request_deserializer=cart__pb2.RemoveCartItemRequest.FromString,
                    response_serializer=cart__pb2.RemoveCartItemResponse.SerializeToString,
            ),
            'ClearCart': grpc.unary_unary_rpc_method_handler(
                    servicer.ClearCart,
                    request_deserializer=cart__pb2.ClearCartRequest.FromString,
                    response_serializer=cart__pb2.ClearCartResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cart.CartService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('cart.CartService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class CartService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetOrCreateCart(request,
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
            '/cart.CartService/GetOrCreateCart',
            cart__pb2.GetOrCreateCartRequest.SerializeToString,
            cart__pb2.GetOrCreateCartResponse.FromString,
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
    def GetCartDetail(request,
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
            '/cart.CartService/GetCartDetail',
            cart__pb2.GetCartDetailRequest.SerializeToString,
            cart__pb2.GetCartDetailResponse.FromString,
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
    def AddToCart(request,
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
            '/cart.CartService/AddToCart',
            cart__pb2.AddToCartRequest.SerializeToString,
            cart__pb2.GetCartItemDetailResponse.FromString,
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
    def ApplyCartItemPromo(request,
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
            '/cart.CartService/ApplyCartItemPromo',
            cart__pb2.ApplyCartItemPromoRequest.SerializeToString,
            cart__pb2.GetCartItemDetailResponse.FromString,
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
    def RemoveCartItem(request,
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
            '/cart.CartService/RemoveCartItem',
            cart__pb2.RemoveCartItemRequest.SerializeToString,
            cart__pb2.RemoveCartItemResponse.FromString,
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
    def ClearCart(request,
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
            '/cart.CartService/ClearCart',
            cart__pb2.ClearCartRequest.SerializeToString,
            cart__pb2.ClearCartResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
