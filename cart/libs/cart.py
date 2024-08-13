from cart.models import Cart
from rest_framework.exceptions import ValidationError

class CartLib:
    @staticmethod
    def get_or_create_cart(user_hash, brand):
        cart, created = Cart.objects.get_or_create(
            user_hash=user_hash,
            brand=brand,
            is_active=True
        )
        return cart

    @staticmethod
    def get_cart_detail(cart_hash):
        try:
            cart = Cart.objects.get(hash=cart_hash)
        except Cart.DoesNotExist:
            raise ValidationError("Cart not found")
        
        return cart

    @staticmethod
    def clear_cart(cart):
        cart.cartitem_set.all().delete()
