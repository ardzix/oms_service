from cart.models import CartItem
from rest_framework.exceptions import ValidationError

class CartItemLib:
    @staticmethod
    def add_to_cart(cart, product, quantity):
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )
        
        if not created:
            cart_item.quantity += quantity

        cart_item.save()
        return cart_item

    @staticmethod
    def apply_cart_item_promo(cart_item, promo_hash):
        cart_item.promo_hash = promo_hash
        cart_item.save()
        return cart_item

    @staticmethod
    def remove_cart_item(cart_item_hash):
        try:
            cart_item = CartItem.objects.get(hash=cart_item_hash)
            cart_item.delete()
        except CartItem.DoesNotExist:
            raise ValidationError("Cart item not found")
