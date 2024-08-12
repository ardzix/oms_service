import grpc
import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oms.settings')
django.setup()

from cart.grpc import cart_pb2, cart_pb2_grpc
from checkout.grpc import checkout_pb2, checkout_pb2_grpc
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

def print_checkout(checkout):
    print(f"Checkout Hash: {checkout.hash}")
    print(f"User Hash: {checkout.user_hash}")
    print(f"Cart Hash: {checkout.cart_hash}")
    print(f"Total Price: {checkout.total_price}")
    print(f"Discount: {checkout.discount}")
    print(f"VAT: {checkout.vat}")
    print(f"Final Price: {checkout.final_price}")
    print(f"Created At: {checkout.created_at}")

def print_invoice(invoice):
    print(f"Invoice Number: {invoice.invoice_number}")
    print(f"Status: {invoice.status}")
    print(f"Created At: {invoice.created_at}")

def run():
    with grpc.insecure_channel(f'{settings.OMS_CART_SERVICE_HOST}:{settings.OMS_CART_SERVICE_PORT}') as cart_channel, \
         grpc.insecure_channel(f'{settings.OMS_CHECKOUT_SERVICE_HOST}:{settings.OMS_CHECKOUT_SERVICE_PORT}') as checkout_channel:
        
        cart_stub = cart_pb2_grpc.CartServiceStub(cart_channel)
        checkout_stub = checkout_pb2_grpc.CheckoutServiceStub(checkout_channel)

        # Get or create a cart by user_hash and brand_hash
        get_or_create_cart_request = cart_pb2.GetOrCreateCartRequest(
            user_hash="055f47c7-76bf-4c41-a89d-f8c9f01f6fd7",
            brand_hash="3e98fa28-0daf-488f-abb5-a280449a6f65"
        )
        cart_response = cart_stub.GetOrCreateCart(get_or_create_cart_request)
        print("Get or Create Cart Response:")
        print_cart(cart_response.cart)

        # Add an item to the cart
        add_to_cart_request = cart_pb2.AddToCartRequest(
            cart_hash=cart_response.cart.hash,
            product_hash="e5712557-2a37-481e-bf69-679c708a7398",
            quantity=4
        )
        add_to_cart_response = cart_stub.AddToCart(add_to_cart_request)
        print("\nAdded to Cart:")
        print_cart_item(add_to_cart_response.cart_item)


        # Apply promo to item cart
        apply_promo_request = cart_pb2.ApplyCartItemPromoRequest(
            cart_item_hash=add_to_cart_response.cart_item.hash,
            promo_hash="b2efe181-b650-4938-bd15-cefcad1d5b32",
        )
        add_to_cart_response = cart_stub.ApplyCartItemPromo(apply_promo_request)
        print("\Promo applied to Cart:")
        print_cart_item(add_to_cart_response.cart_item)

        # Get cart details by cart hash
        get_cart_detail_request = cart_pb2.GetCartDetailRequest(
            cart_hash=cart_response.cart.hash
        )
        cart_detail_response = cart_stub.GetCartDetail(get_cart_detail_request)
        print("\nCart Detail Response:")
        print_cart(cart_detail_response.cart)
        print("\nCart Items:")
        for item in cart_detail_response.cart_items:
            print_cart_item(item)
            print("\n")

        # Create a checkout based on the cart
        create_checkout_request = checkout_pb2.CreateCheckoutRequest(
            cart_hash=cart_response.cart.hash,
            user_hash="055f47c7-76bf-4c41-a89d-f8c9f01f6fd7"
        )
        checkout_response = checkout_stub.CreateCheckout(create_checkout_request)
        print("\nCheckout Created:")
        print_checkout(checkout_response)

        # List all checkouts
        list_checkout_request = checkout_pb2.ListCheckoutsRequest(
            user_hash="055f47c7-76bf-4c41-a89d-f8c9f01f6fd7"
        )
        list_checkouts_response = checkout_stub.ListCheckouts(list_checkout_request)
        print("\nList of Checkouts:")
        for checkout in list_checkouts_response.checkouts:
            print_checkout(checkout)
            print("\n")

        # Get checkout details including the last invoice
        get_checkout_detail_request = checkout_pb2.GetCheckoutDetailRequest(
            hash=checkout_response.hash
        )
        checkout_detail_response = checkout_stub.GetCheckoutDetail(get_checkout_detail_request)
        print("\nCheckout Detail:")
        print(checkout_detail_response.checkout)
        # if checkout_detail_response.last_invoice and checkout_detail_response.last_invoice.invoice_number:
        #     print("Last Invoice:")
        #     print_invoice(checkout_detail_response.last_invoice)

if __name__ == '__main__':
    run()
