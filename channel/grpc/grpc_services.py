import grpc
from concurrent import futures
import logging
from django.core.exceptions import ObjectDoesNotExist
from channel.models import Brand, Channel, Event, Product
from . import oms_channel_pb2, oms_channel_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChannelService(oms_channel_pb2_grpc.ChannelServiceServicer):

    # List all brands
    def ListBrands(self, request, context):
        logger.info("Received ListBrands request")
        brands = Brand.objects.all()
        response = oms_channel_pb2.ListBrandsResponse()
        for brand in brands:
            response.brands.add(
                hash=str(brand.hash),
                name=brand.name,
                description=brand.description,
                is_active=brand.is_active
            )
        return response

    # List all channels
    def ListChannels(self, request, context):
        logger.info("Received ListChannels request")
        channels = Channel.objects.all()
        response = oms_channel_pb2.ListChannelsResponse()
        for channel in channels:
            response.channels.add(
                hash=str(channel.hash),
                name=channel.name,
                description=channel.description,
                brand_hash=str(channel.brand.hash)
            )
        return response

    # List all events
    def ListEvents(self, request, context):
        logger.info("Received ListEvents request")
        events = Event.objects.all()
        response = oms_channel_pb2.ListEventsResponse()
        for event in events:
            response.events.add(
                hash=str(event.hash),
                name=event.name,
                description=event.description,
                start_date=str(event.start_date),
                end_date=str(event.end_date),
                channel_hash=str(event.channel.hash),
                brand_hash=str(event.brand.hash)
            )
        return response

    # Get a product by hash
    def GetProduct(self, request, context):
        logger.info(f"Received GetProduct request for product_hash: {request.product_hash}")
        try:
            product = Product.objects.get(product_hash=request.product_hash)
            return oms_channel_pb2.ProductResponse(
                product_hash=str(product.product_hash),
                channel_hash=str(product.channel.hash),
                event_hash=str(product.event.hash) if product.event else "",
                brand_hash=str(product.brand.hash),
                available=product.available,
                price=float(product.price),
                is_valid=product.is_valid
            )
        except Product.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

    # Create a new product
    def CreateProduct(self, request, context):
        logger.info(f"Received CreateProduct request for product_hash: {request.product_hash}")
        try:
            channel = Channel.objects.get(hash=request.channel_hash)
            brand = Brand.objects.get(hash=request.brand_hash)
            event = Event.objects.get(hash=request.event_hash) if request.event_hash else None

            product = Product.objects.create(
                product_hash=request.product_hash,
                channel=channel,
                event=event,
                brand=brand,
                available=request.available,
                price=request.price,
                is_valid=request.is_valid
            )
            return oms_channel_pb2.ProductResponse(
                product_hash=str(product.product_hash),
                channel_hash=str(product.channel.hash),
                event_hash=str(product.event.hash) if product.event else "",
                brand_hash=str(product.brand.hash),
                available=product.available,
                price=float(product.price),
                is_valid=product.is_valid
            )
        except (Channel.DoesNotExist, Brand.DoesNotExist, Event.DoesNotExist) as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    # Update an existing product
    def UpdateProduct(self, request, context):
        logger.info(f"Received UpdateProduct request for product_hash: {request.product_hash}")
        try:
            product = Product.objects.get(product_hash=request.product_hash)
            product.channel = Channel.objects.get(hash=request.channel_hash)
            product.brand = Brand.objects.get(hash=request.brand_hash)
            product.event = Event.objects.get(hash=request.event_hash) if request.event_hash else None
            product.available = request.available
            product.price = request.price
            product.is_valid = request.is_valid
            product.save()
            return oms_channel_pb2.ProductResponse(
                product_hash=str(product.product_hash),
                channel_hash=str(product.channel.hash),
                event_hash=str(product.event.hash) if product.event else "",
                brand_hash=str(product.brand.hash),
                available=product.available,
                price=float(product.price),
                is_valid=product.is_valid
            )
        except (Product.DoesNotExist, Channel.DoesNotExist, Brand.DoesNotExist, Event.DoesNotExist) as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    # Delete a product
    def DeleteProduct(self, request, context):
        logger.info(f"Received DeleteProduct request for product_hash: {request.product_hash}")
        try:
            product = Product.objects.get(product_hash=request.product_hash)
            product.delete()
            return oms_channel_pb2.Empty()
        except Product.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")


    # List products by channel, event (optional), and brand (optional)
    def ListProducts(self, request, context):
        logger.info(f"Received ListProducts request for channel_hash: {request.channel_hash}, event_hash: {request.event_hash}, brand_hash: {request.brand_hash}")
        products = Product.objects.filter(channel__hash=request.channel_hash)
        
        if request.event_hash:
            products = products.filter(event__hash=request.event_hash)
        
        if request.brand_hash:
            products = products.filter(brand__hash=request.brand_hash)
        
        response = oms_channel_pb2.ListProductsResponse()
        for product in products:
            response.products.add(
                product_hash=str(product.product_hash),
                channel_hash=str(product.channel.hash),
                event_hash=str(product.event.hash) if product.event else "",
                brand_hash=str(product.brand.hash),
                available=product.available,
                price=float(product.price),
                is_valid=product.is_valid
            )
        return response


    # Get a product variant by variant_hash
    def GetProductVariant(self, request, context):
        logger.info(f"Received GetProductVariant request for variant_hash: {request.variant_hash}")
        try:
            variant = Product.objects.get(variant_hash=request.variant_hash)
            return oms_channel_pb2.ProductVariantResponse(
                parent_hash=str(variant.parent.product_hash) if variant.parent else "",
                variant_hash=str(variant.variant_hash),
                channel_hash=str(variant.channel.hash),
                event_hash=str(variant.event.hash) if variant.event else "",
                brand_hash=str(variant.brand.hash),
                available=variant.available,
                price=float(variant.price),
                is_valid=variant.is_valid
            )
        except Product.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product variant not found")

    # Create a new product variant
    def CreateProductVariant(self, request, context):
        logger.info(f"Received CreateProductVariant request for variant_hash: {request.variant_hash}")
        try:
            parent = Product.objects.get(product_hash=request.parent_hash)
            channel = Channel.objects.get(hash=request.channel_hash)
            brand = Brand.objects.get(hash=request.brand_hash)
            event = Event.objects.get(hash=request.event_hash) if request.event_hash else None

            variant = Product.objects.create(
                parent=parent,
                product_hash=None,  # Product hash remains null for variants
                variant_hash=request.variant_hash,
                channel=channel,
                event=event,
                brand=brand,
                available=request.available,
                price=request.price,
                is_valid=request.is_valid
            )
            return oms_channel_pb2.ProductVariantResponse(
                parent_hash=str(variant.parent.product_hash),
                variant_hash=str(variant.variant_hash),
                channel_hash=str(variant.channel.hash),
                event_hash=str(variant.event.hash) if variant.event else "",
                brand_hash=str(variant.brand.hash),
                available=variant.available,
                price=float(variant.price),
                is_valid=variant.is_valid
            )
        except (Product.DoesNotExist, Channel.DoesNotExist, Brand.DoesNotExist, Event.DoesNotExist) as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    # Update an existing product variant
    def UpdateProductVariant(self, request, context):
        logger.info(f"Received UpdateProductVariant request for variant_hash: {request.variant_hash}")
        try:
            variant = Product.objects.get(variant_hash=request.variant_hash)
            variant.parent = Product.objects.get(product_hash=request.parent_hash)
            variant.channel = Channel.objects.get(hash=request.channel_hash)
            variant.brand = Brand.objects.get(hash=request.brand_hash)
            variant.event = Event.objects.get(hash=request.event_hash) if request.event_hash else None
            variant.available = request.available
            variant.price = request.price
            variant.is_valid = request.is_valid
            variant.save()
            return oms_channel_pb2.ProductVariantResponse(
                parent_hash=str(variant.parent.product_hash),
                variant_hash=str(variant.variant_hash),
                channel_hash=str(variant.channel.hash),
                event_hash=str(variant.event.hash) if variant.event else "",
                brand_hash=str(variant.brand.hash),
                available=variant.available,
                price=float(variant.price),
                is_valid=variant.is_valid
            )
        except (Product.DoesNotExist, Channel.DoesNotExist, Brand.DoesNotExist, Event.DoesNotExist) as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    # Delete a product variant
    def DeleteProductVariant(self, request, context):
        logger.info(f"Received DeleteProductVariant request for variant_hash: {request.variant_hash}")
        try:
            variant = Product.objects.get(variant_hash=request.variant_hash)
            variant.delete()
            return oms_channel_pb2.Empty()
        except Product.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product variant not found")

    # List product variants by parent hash
    def ListProductVariants(self, request, context):
        logger.info(f"Received ListProductVariants request for parent_hash: {request.parent_hash}")
        variants = Product.objects.filter(parent__product_hash=request.parent_hash)
        response = oms_channel_pb2.ListProductVariantsResponse()
        for variant in variants:
            response.variants.add(
                parent_hash=str(variant.parent.product_hash) if variant.parent else "",
                variant_hash=str(variant.variant_hash),
                channel_hash=str(variant.channel.hash),
                event_hash=str(variant.event.hash) if variant.event else "",
                brand_hash=str(variant.brand.hash),
                available=variant.available,
                price=float(variant.price),
                is_valid=variant.is_valid
            )
        return response