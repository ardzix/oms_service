import grpc
import os
import django
from datetime import datetime, timedelta

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oms.settings')
django.setup()
from django.conf import settings

from cart.grpc import cart_pb2, cart_pb2_grpc

# gRPC client setup
class CartClient:
    def __init__(self, host, port):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = cart_pb2_grpc.CartServiceStub(self.channel)

    def get_or_create_cart(self, user_hash, brand_hash):
        request = cart_pb2.GetOrCreateCartRequest(user_hash=user_hash, brand_hash=brand_hash)
        print(f"Sending GetOrCreateCart request: {request}")
        response = self.stub.GetOrCreateCart(request)
        print(f"Received GetOrCreateCart response: {response}")
        return response.cart.hash

    def get_cart_detail(self, cart_hash):
        request = cart_pb2.GetCartDetailRequest(cart_hash=cart_hash)
        print(f"Sending GetCartDetail request: {request}")
        response = self.stub.GetCartDetail(request)
        print(f"Received GetCartDetail response: {response}")
        return response

    def add_to_cart(self, cart_hash, product_hash, quantity):
        request = cart_pb2.AddToCartRequest(cart_hash=cart_hash, product_hash=product_hash, quantity=quantity)
        print(f"Sending AddToCart request: {request}")
        response = self.stub.AddToCart(request)
        print(f"Received AddToCart response: {response}")
        return response.cart_item.hash

    def apply_cart_item_promo(self, cart_item_hash, promo_hash):
        request = cart_pb2.ApplyCartItemPromoRequest(cart_item_hash=cart_item_hash, promo_hash=promo_hash)
        print(f"Sending ApplyCartItemPromo request: {request}")
        response = self.stub.ApplyCartItemPromo(request)
        print(f"Received ApplyCartItemPromo response: {response}")

    def apply_cart_promo(self, cart_hash, promo_hash):
        request = cart_pb2.ApplyCartPromoRequest(cart_hash=cart_hash, promo_hash=promo_hash)
        print(f"Sending ApplyCartPromo request: {request}")
        response = self.stub.ApplyCartPromo(request)
        print(f"Received ApplyCartPromo response: {response}")

    def remove_cart_item(self, cart_item_hash):
        request = cart_pb2.RemoveCartItemRequest(cart_item_hash=cart_item_hash)
        print(f"Sending RemoveCartItem request: {request}")
        response = self.stub.RemoveCartItem(request)
        print(f"Received RemoveCartItem response: {response}")

    def clear_cart(self, cart_hash):
        request = cart_pb2.ClearCartRequest(cart_hash=cart_hash)
        print(f"Sending ClearCart request: {request}")
        response = self.stub.ClearCart(request)
        print(f"Received ClearCart response: {response}")


# Test script
def run_tests():
    # Setup client
    host = settings.OMS_CART_SERVICE_HOST
    port = settings.OMS_CART_SERVICE_PORT
    client = CartClient(host, port)

    # Test GetOrCreateCart
    user_hash = "3e98fa28-0daf-488f-abb5-a280449a6f65"
    brand_hash = "3e98fa28-0daf-488f-abb5-a280449a6f65"
    cart_hash = str(client.get_or_create_cart(user_hash, brand_hash))

    # Add item to the cart
    product_hash = "fbb7d89c-be1a-47ac-bf2d-7ecce29295ab"  # Example product hash, replace with actual
    quantity = 2
    cart_item_hash = client.add_to_cart(cart_hash, product_hash, quantity)
    print("cart item hash: ", cart_item_hash)

    # Add item to the cart
    product_hash2 = "fbb7d89c-be1a-47ac-bf2d-7ecce29295ac"  # Example product hash, replace with actual
    quantity = 3
    cart_item_hash2 = client.add_to_cart(cart_hash, product_hash2, quantity)

    # Get cart detail
    client.get_cart_detail(cart_hash)

    # Apply promo to cart item
    promo_hash = "0c773d12-699a-4267-9e72-3251bb506872"  # Example promo hash, replace with actual
    client.apply_cart_item_promo(cart_item_hash, promo_hash)

    # Apply promo to cart
    promo_hash = "73807f19-7c25-497a-8d4c-733835e0761d"  # Example promo hash, replace with actual
    client.apply_cart_promo(cart_hash, promo_hash)

    # # Remove cart item
    # client.remove_cart_item(cart_item_hash)

    # Clear cart
    # client.clear_cart(cart_hash)


if __name__ == '__main__':
    run_tests()
