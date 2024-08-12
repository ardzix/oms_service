import grpc
import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oms.settings')
django.setup()

from cart.grpc import cart_pb2, cart_pb2_grpc
from django.conf import settings

def print_cart(cart):
    print(f"Cart Hash: {cart.hash}")
    print(f"User Hash: {cart.user_hash}")
    print(f"Brand Hash: {cart.brand_hash}")
    print(f"Is Active: {cart.is_active}")
    print(f"Created At: {cart.created_at}")
    print(f"Updated At: {cart.updated_at}")

def print_cart_item(cart_item):
    print(f"Product Hash: {cart_item.product_hash}")
    print(f"Quantity: {cart_item.quantity}")
    print(f"Price: {cart_item.price}")
    print(f"Promo Hash: {cart_item.promo_hash}")
    print(f"Modified Price: {cart_item.modified_price}")
    print(f"Is BOGO: {cart_item.is_bogo}")
    print(f"BOGO Quantity: {cart_item.bogo_quantity}")
    print(f"Is Point Purchase: {cart_item.is_point_purchase}")
    print(f"Points Payable: {cart_item.points_payable}")

def run():
    with grpc.insecure_channel(f'{settings.OMS_CART_SERVICE_HOST}:{settings.OMS_CART_SERVICE_PORT}') as channel:
        stub = cart_pb2_grpc.CartServiceStub(channel)

        # Get or create a cart by user_hash and brand_hash
        get_or_create_cart_request = cart_pb2.GetOrCreateCartRequest(
            user_hash="055f47c7-76bf-4c41-a89d-f8c9f01f6fd7",
            brand_hash="fbbd1a17-b3dc-4cab-bde3-d82716f53cd3"
        )
        cart_response = stub.GetOrCreateCart(get_or_create_cart_request)
        print("Get or Create Cart Response:")
        print_cart(cart_response.cart)

        # Add an item to the cart
        add_to_cart_request = cart_pb2.AddToCartRequest(
            cart_hash=cart_response.cart.hash,
            product_hash="fbbd1a17-b3dc-4cab-bde3-d82716f53cd3",
            quantity=2
        )
        add_to_cart_response = stub.AddToCart(add_to_cart_request)
        print("\nAdded to Cart:")
        print_cart_item(add_to_cart_response.cart_item)

        # Get cart details by cart hash
        get_cart_detail_request = cart_pb2.GetCartDetailRequest(
            cart_hash=cart_response.cart.hash
        )
        cart_detail_response = stub.GetCartDetail(get_cart_detail_request)
        print("\nCart Detail Response:")
        print_cart(cart_detail_response.cart)
        print("\nCart Items:")
        for item in cart_detail_response.cart_items:
            print_cart_item(item)
            print("\n")

        # Remove an item from the cart
        # remove_cart_item_request = cart_pb2.RemoveCartItemRequest(
        #     cart_hash=cart_response.cart.hash,
        #     product_hash="fbbd1a17-b3dc-4cab-bde3-d82716f53cd3"
        # )
        # remove_cart_item_response = stub.RemoveCartItem(remove_cart_item_request)
        # print("\nRemoved Item from Cart:")
        # print(f"Success: {remove_cart_item_response.success}")

        # Clear all items from the cart
        # clear_cart_request = cart_pb2.ClearCartRequest(
        #     cart_hash=cart_response.cart.hash
        # )
        # clear_cart_response = stub.ClearCart(clear_cart_request)
        # print("\nCleared Cart:")
        # print(f"Success: {clear_cart_response.success}")

        # Get cart details after clearing
        cart_detail_response_after_clear = stub.GetCartDetail(get_cart_detail_request)
        print("\nCart Detail Response After Clearing:")
        print_cart(cart_detail_response_after_clear.cart)
        print("\nCart Items After Clearing:")
        for item in cart_detail_response_after_clear.cart_items:
            print_cart_item(item)
            print("\n")

if __name__ == '__main__':
    run()
