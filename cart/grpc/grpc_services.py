import grpc
import logging
from django.utils.timezone import now
from cart.models import Cart, CartItem
from channel.models import Brand, Product
from services.channel.channel_client import ChannelClient
from . import cart_pb2, cart_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CartService(cart_pb2_grpc.CartServiceServicer):

    def GetOrCreateCart(self, request, context):
        logger.info(f"Received GetOrCreateCart request with user_hash: {request.user_hash} and brand_hash: {request.brand_hash}")
        channel_client = ChannelClient()
        brand_response = channel_client.get_brand(request.brand_hash)
        if not brand_response:
            context.abort(grpc.StatusCode.NOT_FOUND, "Brand not found")

        brand, created = Brand.objects.get_or_create(
            hash=request.brand_hash,
            defaults={
                "name": brand_response.name,
                "description": brand_response.description,
                "is_active": brand_response.is_active
            },
        )

        cart, created = Cart.objects.get_or_create(
            user_hash=request.user_hash,
            brand=brand,
            is_active=True
        )
        
        cart_response = cart_pb2.Cart(
            hash=str(cart.hash),
            user_hash=cart.user_hash,
            brand_hash=request.brand_hash,
            is_active=cart.is_active,
            created_at=str(cart.created_at),
            updated_at=str(cart.updated_at)
        )
        logger.info(f"Returning Cart with hash: {cart.hash}")
        return cart_pb2.GetOrCreateCartResponse(cart=cart_response)

    def GetCartDetail(self, request, context):
        logger.info(f"Received GetCartDetail request with cart_hash: {request.cart_hash}")
        try:
            cart = Cart.objects.get(hash=request.cart_hash)
        except Cart.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart not found")

        cart_items = CartItem.objects.filter(cart=cart)
        cart_items_response = [
            cart_pb2.CartItem(
                product_hash=item.product.product_hash,
                quantity=item.quantity,
                price=float(item.price),
                promo_hash=item.promo_hash,
                modified_price=float(item.modified_price),
                is_bogo=item.is_bogo,
                bogo_quantity=item.bogo_quantity,
                is_point_purchase=item.is_point_purchase,
                points_payable=item.points_payable
            )
            for item in cart_items
        ]
        
        cart_response = cart_pb2.Cart(
            hash=str(cart.hash),
            user_hash=cart.user_hash,
            brand_hash=str(cart.brand.hash),
            is_active=cart.is_active,
            created_at=str(cart.created_at),
            updated_at=str(cart.updated_at)
        )
        
        logger.info(f"Returning details for Cart with hash: {cart.hash}")
        return cart_pb2.GetCartDetailResponse(cart=cart_response, cart_items=cart_items_response)

    def AddToCart(self, request, context):
        logger.info(f"Received AddToCart request for cart_hash: {request.cart_hash}, product_hash: {request.product_hash}, quantity: {request.quantity}")
        try:
            cart = Cart.objects.get(hash=request.cart_hash)
        except Cart.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart not found")

        try:
            product = Product.objects.get(product_hash=request.product_hash)
        except Product.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': request.quantity, 'price': product.price}
        )

        if not created:
            cart_item.quantity += request.quantity

        cart_item.save()

        cart_item_response = cart_pb2.CartItem(
            product_hash=cart_item.product.product_hash,
            quantity=cart_item.quantity,
            price=float(cart_item.price),
            promo_hash=cart_item.promo_hash,
            modified_price=float(cart_item.modified_price) if cart_item.modified_price else cart_item.price,
            is_bogo=cart_item.is_bogo,
            bogo_quantity=cart_item.bogo_quantity,
            is_point_purchase=cart_item.is_point_purchase,
            points_payable=cart_item.points_payable,
            hash=str(cart_item.hash)
        )

        logger.info(f"Item added to cart with cart_hash: {request.cart_hash}")
        return cart_pb2.GetCartItemDetailResponse(cart_item=cart_item_response)
    
    def ApplyCartItemPromo(self, request, context):
        logger.info(f"Received ApplyCartItemPromo request for cart_item_hash: {request.cart_item_hash}, promo_hash: {request.promo_hash}")
        try:
            cart_item = CartItem.objects.get(hash=request.cart_item_hash)
            cart_item.promo_hash = request.promo_hash
            cart_item.save()
        except CartItem.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart item not found")
            return cart_pb2.RemoveCartItemResponse(success=False)
        
        cart_item_response = cart_pb2.CartItem(
            product_hash=cart_item.product.product_hash,
            quantity=cart_item.quantity,
            price=float(cart_item.price),
            promo_hash=cart_item.promo_hash,
            modified_price=float(cart_item.modified_price) if cart_item.modified_price else cart_item.price,
            is_bogo=cart_item.is_bogo,
            bogo_quantity=cart_item.bogo_quantity,
            is_point_purchase=cart_item.is_point_purchase,
            points_payable=cart_item.points_payable,
            hash=str(cart_item.hash)
        )

        logger.info(f"Item promo {request.promo_hash} has been added to cart item with hash: {request.cart_item_hash}")
        return cart_pb2.GetCartItemDetailResponse(cart_item=cart_item_response)

    def RemoveCartItem(self, request, context):
        logger.info(f"Received RemoveCartItem request for cart_item_hash: {request.cart_item_hash}")
        try:
            cart_item = CartItem.objects.get(hasattr=request.cart_item_hash)
            cart_item.delete()
            logger.info(f"Removed item {request.cart_item_hash} from cart {request.cart_hash}")
            return cart_pb2.RemoveCartItemResponse(success=True)
        except CartItem.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart item not found")
            return cart_pb2.RemoveCartItemResponse(success=False)

    def ClearCart(self, request, context):
        logger.info(f"Received ClearCart request for cart_hash: {request.cart_hash}")
        try:
            cart = Cart.objects.get(hash=request.cart_hash)
        except Cart.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart not found")

        CartItem.objects.filter(cart=cart).delete()
        logger.info(f"Cleared all items from cart {request.cart_hash}")
        return cart_pb2.ClearCartResponse(success=True)
