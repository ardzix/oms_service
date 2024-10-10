import grpc
import logging
from cart.models import Cart, CartItem
from channel.models import Brand, Product
from django.db import transaction
from . import cart_pb2, cart_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CartService(cart_pb2_grpc.CartServiceServicer):

    def GetOrCreateCart(self, request, context):
        logger.info(f"Received GetOrCreateCart request with user_hash: {request.user_hash} and brand_hash: {request.brand_hash}")

        try:
            brand = Brand.objects.get(hash=request.brand_hash)
        except Brand.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Brand not found")

        # Get or create a cart for the user and brand
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
            updated_at=str(cart.updated_at),
            coupon_code=cart.coupon_code,
            promo_hash=cart.promo_hash,
            available_promos=cart.available_promos,
        )

        logger.info(f"Returning Cart with hash: {cart.hash}")
        return cart_pb2.GetOrCreateCartResponse(cart=cart_response)

    def GetCartDetail(self, request, context):
        logger.info(f"Received GetCartDetail request with cart_hash: {request.cart_hash}")
        try:
            cart = Cart.objects.get(hash=request.cart_hash)
        except Cart.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart not found")

        cart_items_response = [
            cart_pb2.CartItem(
                product_hash=str(item.product.hash),
                quantity=item.quantity,
                price=float(item.price),
                promo_hash=item.promo_hash,
                modified_price=float(item.modified_price) if item.modified_price else float(item.price),
                hash=str(item.hash),
                coupon_code=item.coupon_code,
                available_promos=item.available_promos,
            )
            for item in cart.cart_items.all()
        ]

        cart_response = cart_pb2.Cart(
            hash=str(cart.hash),
            user_hash=cart.user_hash,
            brand_hash=str(cart.brand.hash),
            is_active=cart.is_active,
            created_at=str(cart.created_at),
            updated_at=str(cart.updated_at),
            coupon_code=cart.coupon_code,
            promo_hash=cart.promo_hash,
            available_promos=cart.available_promos
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
            product = Product.objects.get(hash=request.product_hash)
        except Product.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

        # Add or update cart item
        cart_item, created = CartItem.objects.update_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': request.quantity, 'price': product.price}
        )
        print("\n\nCart (Item)")
        print(cart_item)

        cart_item_response = cart_pb2.CartItem(
            product_hash=str(cart_item.product.hash),
            quantity=cart_item.quantity,
            price=float(cart_item.price),
            promo_hash=cart_item.promo_hash,
            modified_price=float(cart_item.modified_price) if cart_item.modified_price else cart_item.price,
            hash=str(cart_item.hash),
            coupon_code=cart_item.coupon_code,
            available_promos=cart_item.available_promos,
        )

        logger.info(f"Item added to cart with cart_hash: {request.cart_hash}")
        return cart_pb2.GetCartItemDetailResponse(cart_item=cart_item_response)

    def ApplyCartItemPromo(self, request, context):
        logger.info(f"Received ApplyCartItemPromo request for cart_item_hash: {request.cart_item_hash}, promo_hash: {request.promo_hash}")
        try:
            cart_item = CartItem.objects.get(hash=request.cart_item_hash)
        except CartItem.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart item not found")

        # Validate promo availability
        if cart_item.available_promos and request.promo_hash not in cart_item.available_promos.split(','):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Promo hash is not available for this cart item")

        # Apply promo to cart item
        cart_item.promo_hash = request.promo_hash

        #modify later:
        cart_item.modified_price = 15

        cart_item.save()

        cart_item_response = cart_pb2.CartItem(
            product_hash=str(cart_item.product.hash),
            quantity=cart_item.quantity,
            price=float(cart_item.price),
            promo_hash=cart_item.promo_hash,
            modified_price=float(cart_item.modified_price) if cart_item.modified_price else cart_item.price,
            hash=str(cart_item.hash),
            coupon_code=cart_item.coupon_code,
            available_promos=cart_item.available_promos,
        )

        logger.info(f"Applied promo {request.promo_hash} to cart item with hash: {request.cart_item_hash}")
        return cart_pb2.GetCartItemDetailResponse(cart_item=cart_item_response)

    def ApplyCartPromo(self, request, context):
        logger.info(f"Received ApplyCartPromo request for cart_hash: {request.cart_hash}, promo_hash: {request.promo_hash}")
        try:
            cart = Cart.objects.get(hash=request.cart_hash)
        except Cart.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart not found")

        # Validate promo availability
        if cart.available_promos and request.promo_hash not in cart.available_promos.split(','):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Promo hash is not available for this cart")

        # Apply promo to the cart
        cart.promo_hash = request.promo_hash
        cart.save()

        cart_response = cart_pb2.Cart(
            hash=str(cart.hash),
            user_hash=cart.user_hash,
            brand_hash=str(cart.brand.hash),
            is_active=cart.is_active,
            created_at=str(cart.created_at),
            updated_at=str(cart.updated_at),
            coupon_code=cart.coupon_code,
            promo_hash=cart.promo_hash,
            available_promos=cart.available_promos
        )

        logger.info(f"Applied promo {request.promo_hash} to cart with hash: {request.cart_hash}")
        return cart_pb2.GetCartDetailResponse(cart=cart_response)

    def RemoveCartItem(self, request, context):
        logger.info(f"Received RemoveCartItem request for cart_item_hash: {request.cart_item_hash}")
        try:
            cart_item = CartItem.objects.get(hash=request.cart_item_hash)
            cart_item.delete()
            logger.info(f"Removed item {request.cart_item_hash} from cart")
            return cart_pb2.RemoveCartItemResponse(success=True)
        except CartItem.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart item not found")

    def ClearCart(self, request, context):
        logger.info(f"Received ClearCart request for cart_hash: {request.cart_hash}")
        try:
            cart = Cart.objects.get(hash=request.cart_hash)
        except Cart.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart not found")

        # Clear all cart items
        cart.cart_items.all().delete()
        logger.info(f"Cleared all items from cart {request.cart_hash}")
        return cart_pb2.ClearCartResponse(success=True)
