import grpc
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import CartItem
from services.promo import promo_pb2
from services.promo.promo_client import PromoClient  # Assuming you have a PromoClient

@receiver(post_save, sender=CartItem)
def check_promos_for_cart_and_item(sender, instance, created, **kwargs):
    """
    Signal to check available promotions when a CartItem is created or updated.
    """
    if created:
        print("RUnning signal for item ", instance)
        # Initialize PromoClient
        promo_client = PromoClient()

        # Get the cart and its items
        cart = instance.cart
        cart_items = CartItem.objects.filter(cart=cart)

        # Prepare product hashes and quantities for the entire cart
        items_list = [
            promo_pb2.Item(
                product_hash=str(item.product.hash),
                quantity=item.quantity,
                unit_price=float(item.price)
            )
            for item in cart_items
        ]
        print(items_list)
        # Call CheckItemsPromos for the entire cart
        cart_promo_request = promo_pb2.CheckItemsPromosRequest(
            items=items_list,
            coupon_code=cart.coupon_code if cart.coupon_code else "",
            subtotal=sum(item.price * item.quantity for item in cart_items)
        )

        try:
            cart_promo_response = promo_client.stub.CheckItemsPromos(cart_promo_request)

            # Save available promos for the cart (if any)
            available_promos = ",".join([promo.promo_hash for promo in cart_promo_response.bundle_promos])
            cart.available_promos = available_promos
            cart.save()

        except grpc.RpcError as e:
            print(f"Error checking cart promos: {e.details()}")

        # Call CheckItemPromo for the individual cart item
        item_promo_request = promo_pb2.CheckItemPromoRequest(
            product_hash=str(instance.product.hash),
            coupon_code=instance.coupon_code if instance.coupon_code else ""
        )

        print("\n\nItem promo request:")
        print(item_promo_request)

        try:
            item_promo_response = promo_client.stub.CheckItemPromo(item_promo_request)
            print("\n\nItem promo responses:")
            print(item_promo_response)

            # Save available promos for the individual cart item
            if item_promo_response.discount_promo.promo_hash:
                instance.available_promos = item_promo_response.discount_promo.promo_hash
            elif item_promo_response.point_purchase_promo.promo_hash:
                instance.available_promos = item_promo_response.point_purchase_promo.promo_hash
            instance.save()

        except grpc.RpcError as e:
            print(f"Error checking item promo: {e.details()}")
