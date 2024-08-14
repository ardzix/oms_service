import grpc
import logging
from rest_framework.exceptions import ValidationError
from channel.models import Brand, Channel, Event, Product
from ..serializers.brand import BrandSerializer
from ..serializers.channel import ChannelSerializer
from ..serializers.event import EventSerializer
from ..serializers.product import ProductSerializer
from ..serializers.product_variant import ProductVariantSerializer
from ..libs.brand import BrandLib
from ..libs.channel import ChannelLib
from ..libs.event import EventLib
from ..libs.product import ProductLib
from ..libs.product_variant import ProductVariantLib
from . import oms_channel_pb2, oms_channel_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChannelService(oms_channel_pb2_grpc.ChannelServiceServicer):

    def ListBrands(self, request, context):
        logger.info("Received ListBrands request")
        brands = BrandLib.list_brands()
        serializer = BrandSerializer(brands, many=True)
        response = oms_channel_pb2.ListBrandsResponse()
        
        for brand_data in serializer.data:
            brand_message = oms_channel_pb2.Brand(
                hash=brand_data['hash'],
                name=brand_data['name'],
                description=brand_data['description'],
                is_active=brand_data['is_active']
            )
            response.brands.append(brand_message)
        
        return response

    def ListChannels(self, request, context):
        logger.info("Received ListChannels request")
        channels = ChannelLib.list_channels()
        serializer = ChannelSerializer(channels, many=True)
        response = oms_channel_pb2.ListChannelsResponse()
        
        for channel_data in serializer.data:
            channel_message = oms_channel_pb2.Channel(
                hash=channel_data['hash'],
                name=channel_data['name'],
                description=channel_data['description'],
                brand_hash=str(channel_data['brand'])  # Ensure the brand_hash is a string
            )
            response.channels.append(channel_message)
        
        return response

    def ListEvents(self, request, context):
        logger.info("Received ListEvents request")
        events = EventLib.list_events()
        serializer = EventSerializer(events, many=True)
        response = oms_channel_pb2.ListEventsResponse()
        
        for event_data in serializer.data:
            event_message = oms_channel_pb2.Event(
                hash=event_data['hash'],
                name=event_data['name'],
                description=event_data['description'],
                start_date=event_data['start_date'],
                end_date=event_data['end_date'],
                channel_hash=str(event_data['channel']),
                brand_hash=str(event_data['brand'])
            )
            response.events.append(event_message)
        
        return response

    def GetProduct(self, request, context):
        logger.info(f"Received GetProduct request for hash: {request.hash}")
        try:
            product = ProductLib.get_product_by_hash(request.hash)
            serializer = ProductSerializer(product)
            product_data = serializer.data
            return oms_channel_pb2.ProductResponse(
                hash=product_data['hash'],
                product_hash=product_data['product_hash'],
                channel_hash=str(product_data['channel']),
                event_hash=str(product_data['event']) if product_data['event'] else "",
                brand_hash=str(product_data['brand']),
                available=product_data['available'],
                price=float(product_data['price']),
                is_valid=product_data['is_valid']
            )
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except Exception as e:
            context.abort(grpc.StatusCode.ABORTED, str(e))

    def CreateProduct(self, request, context):
        logger.info(f"Received CreateProduct request for product_hash: {request.product_hash}")
        serializer = ProductSerializer(data={
            'product_hash': request.product_hash,
            'channel': Channel.objects.get(hash=request.channel_hash).pk if request.channel_hash else None,
            'event': Event.objects.get(hash=request.event_hash).pk if request.event_hash else None,
            'brand': Brand.objects.get(hash=request.brand_hash).pk if request.brand_hash else None,
            'available': request.available,
            'price': request.price,
            'is_valid': request.is_valid,
        })

        if serializer.is_valid():
            product = serializer.save()
            return oms_channel_pb2.ProductResponse(
                product_hash=product.product_hash,
                channel_hash=str(product.channel.hash),
                event_hash=str(product.event.hash) if product.event else "",
                brand_hash=str(product.brand.hash),
                available=product.available,
                price=float(product.price),
                is_valid=product.is_valid,
                hash=str(product.hash)
            )
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))

    def UpdateProduct(self, request, context):
        logger.info(f"Received UpdateProduct request for hash: {request.hash}")
        try:
            product = ProductLib.get_product_by_hash(request.hash)
            serializer = ProductSerializer(product, data={
                'channel': Channel.objects.get(hash=request.channel_hash).pk if request.channel_hash else None,
                'event': Event.objects.get(hash=request.event_hash).pk if request.event_hash else None,
                'brand': Brand.objects.get(hash=request.brand_hash).pk if request.brand_hash else None,
                'available': request.available,
                'price': request.price,
                'is_valid': request.is_valid,
                'hash': request.hash,
            }, partial=True)

            if serializer.is_valid():
                product = serializer.save()
                return oms_channel_pb2.ProductResponse(
                    product_hash=product.product_hash,
                    channel_hash=str(product.channel.hash),
                    event_hash=str(product.event.hash) if product.event else "",
                    brand_hash=str(product.brand.hash),
                    available=product.available,
                    price=float(product.price),
                    is_valid=product.is_valid,
                    hash=str(product.hash),
                )
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def DeleteProduct(self, request, context):
        logger.info(f"Received DeleteProduct request for product_hash: {request.hash}")
        try:
            ProductLib.delete_product_by_hash(request.hash)
            return oms_channel_pb2.Empty()
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def ListProducts(self, request, context):
        logger.info(f"Received ListProducts request for channel_hash: {request.channel_hash}, event_hash: {request.event_hash}, brand_hash: {request.brand_hash}")
        try:
            products = ProductLib.list_products(
                channel_hash=request.channel_hash, 
                event_hash=request.event_hash, 
                brand_hash=request.brand_hash
            )
            serializer = ProductSerializer(products, many=True)
            response = oms_channel_pb2.ListProductsResponse()

            for product_data in serializer.data:
                product_message = oms_channel_pb2.ProductResponse(
                    product_hash=product_data['product_hash'],
                    channel_hash=str(product_data['channel']),
                    event_hash=str(product_data['event']) if product_data['event'] else "",
                    brand_hash=str(product_data['brand']),
                    available=product_data['available'],
                    price=float(product_data['price']),
                    is_valid=product_data['is_valid'],
                    hash=product_data['hash'],
                )
                response.products.append(product_message)

            return response
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def GetProductVariant(self, request, context):
        logger.info(f"Received GetProductVariant request for hash: {request.hash}")
        try:
            variant = ProductLib.get_product_by_hash(request.hash)
            serializer = ProductVariantSerializer(variant)
            variant_data = serializer.data
            return oms_channel_pb2.ProductVariantResponse(
                parent_hash=str(variant_data['parent_hash']),
                variant_hash=variant_data['variant_hash'],
                channel_hash=str(variant_data['channel']),
                event_hash=str(variant_data['event']),
                brand_hash=str(variant_data['brand']),
                available=variant_data['available'],
                price=float(variant_data['price']),
                is_valid=variant_data['is_valid'],
                hash=variant_data['hash']
            )
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def CreateProductVariant(self, request, context):
        logger.info(f"Received CreateProductVariant request for variant_hash: {request.variant_hash}")

        try:
            serializer = ProductVariantSerializer(data={
                'parent': ProductLib.get_product_by_hash(request.parent_hash).pk,
                'variant_hash': request.variant_hash,
                'channel': Channel.objects.get(hash=request.channel_hash).pk if request.channel_hash else None,
                'event': Event.objects.get(hash=request.event_hash).pk if request.event_hash else None,
                'brand': Brand.objects.get(hash=request.brand_hash).pk if request.brand_hash else None,
                'available': request.available,
                'price': request.price,
                'is_valid': request.is_valid,
            })
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

        if serializer.is_valid():
            variant = serializer.save()
            return oms_channel_pb2.ProductVariantResponse(
                parent_hash=str(variant.parent.product_hash) if variant.parent else "",
                variant_hash=variant.variant_hash,
                channel_hash=str(variant.channel.hash),
                event_hash=str(variant.event.hash) if variant.event else "",
                brand_hash=str(variant.brand.hash),
                available=variant.available,
                price=float(variant.price),
                is_valid=variant.is_valid,
                hash=str(variant.hash)
            )
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))

    def UpdateProductVariant(self, request, context):
        logger.info(f"Received UpdateProductVariant request for hash: {request.hash}")
        try:
            variant = ProductLib.get_product_by_hash(request.hash)
            serializer = ProductVariantSerializer(variant, data={
                'parent': ProductLib.get_product_by_hash(request.parent_hash).pk,
                'channel': Channel.objects.get(hash=request.channel_hash).pk if request.channel_hash else None,
                'event': Event.objects.get(hash=request.event_hash).pk if request.event_hash else None,
                'brand': Brand.objects.get(hash=request.brand_hash).pk if request.brand_hash else None,
                'available': request.available,
                'price': request.price,
                'is_valid': request.is_valid,
                'hash': request.hash,
            }, partial=True)

            if serializer.is_valid():
                variant = serializer.save()
                return oms_channel_pb2.ProductVariantResponse(
                    parent_hash=str(variant.parent.product_hash) if variant.parent else "",
                    variant_hash=variant.variant_hash,
                    channel_hash=str(variant.channel.hash),
                    event_hash=str(variant.event.hash) if variant.event else "",
                    brand_hash=str(variant.brand.hash),
                    available=variant.available,
                    price=float(variant.price),
                    is_valid=variant.is_valid,
                    hash=str(variant.hash)
                )
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def DeleteProductVariant(self, request, context):
        logger.info(f"Received DeleteProductVariant request for hash: {request.hash}")
        try:
            ProductLib.delete_product_by_hash(request.hash)
            return oms_channel_pb2.Empty()
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def ListProductVariants(self, request, context):
        logger.info(f"Received ListProductVariants request for parent_hash: {request.parent_hash}")
        try:
            variants = ProductVariantLib.list_variants_by_parent_hash(request.parent_hash)
            serializer = ProductVariantSerializer(variants, many=True)
            response = oms_channel_pb2.ListProductVariantsResponse()

            for variant_data in serializer.data:
                variant_message = oms_channel_pb2.ProductVariantResponse(
                    parent_hash=str(variant_data['parent']) if variant_data['parent'] else "",
                    variant_hash=variant_data['variant_hash'],
                    channel_hash=str(variant_data['channel']),
                    event_hash=str(variant_data['event']) if variant_data['event'] else "",
                    brand_hash=str(variant_data['brand']),
                    available=variant_data['available'],
                    price=float(variant_data['price']),
                    is_valid=variant_data['is_valid'],
                    hash=variant_data['hash'],
                )
                response.variants.append(variant_message)

            return response
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))
