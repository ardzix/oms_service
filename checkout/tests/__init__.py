import unittest
from django.test import TestCase
from django.db import transaction
from services.catalogue.catalogue_client import CatalogueClient
from services.promo.promo_client import PromoClient
from channel.models import Brand, Channel, Product
from cart.models import Cart, CartItem, BuyXGetYPromo
from checkout.models import Checkout, Invoice

class OMSClientTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.masterdata_client = CatalogueClient()
        cls.promo_client = PromoClient()

    def setUp(self):
        # Create test data
        self.brand = Brand.objects.create(name="Brand A", description="Brand A Description")
        self.channel = Channel.objects.create(name="Tokopedia", description="Tokopedia Channel", brand=self.brand)

        product_y =  self.masterdata_client.get_product(product_hash='fa6df1f2-0045-47dc-a32a-3e138f2a9186')
        self.product_y = Product.objects.create(product_hash=product_y.hash, channel=self.channel, brand=self.brand, price=product_y.base_price)
        product_x =  self.masterdata_client.get_product(product_hash='e5712557-2a37-481e-bf69-679c708a7398')
        self.product_x = Product.objects.create(product_hash=product_x.hash, channel=self.channel, brand=self.brand, price=product_x.base_price)

        self.cart = Cart.objects.create(user_hash='test_user_hash', brand=self.brand)
        self.cart_item_x = CartItem.objects.create(cart=self.cart, product=self.product_x, quantity=2, promo_hash='6fa12a6b-dd3a-499e-a260-7d6dade2b7b0')
        self.cart_item_y = CartItem.objects.create(cart=self.cart, product=self.product_y, quantity=2)

    def test_cart_item_creation_with_promo(self):
        # Validate CartItem creation with a valid promo hash
        self.cart_item_x.save()
        print(f"Test cart item creation with:")
        print(f"- promo {self.cart_item_x.promo_hash}")
        print(f"- product: {self.cart_item_x.product.product_hash}")
        print(f"- product price: {self.cart_item_x.product.price}")


        promo_client = PromoClient()
        promo_response = promo_client.get_promo_by_hash(self.cart_item_x.promo_hash)
        self.assertEqual(self.cart_item_x.modified_price, promo_response.discount_promos[0].final_price)
        print(f"CartItem saved: Modified Price: {self.cart_item_x.modified_price}")
        print("==================\n")

    # def test_buy_x_get_y_promo(self):
    #     # Test Buy X Get Y promo handling
    #     self.cart_item_x.save()
    #     self.cart_item_y.save()
    #     print("Test Buy X Get Y promo with:")
    #     print(f"- X product: {self.cart_item_x.product.product_hash}")
    #     print(f"- Y product: {self.cart_item_y.product.product_hash}")
    #     print(f"- Y product price: {self.cart_item_y.product.price}")

    #     buy_x_get_y = BuyXGetYPromo.objects.filter(required_product=self.product_x).first()
    #     promo_hash = buy_x_get_y.promo_hash

    #     promo_client = PromoClient()
    #     promo_response = promo_client.get_promo_by_hash(promo_hash)

    #     self.assertEqual(self.cart_item_y.modified_price, promo_response.buy_x_get_y_promos[0].discounted_price)
    #     self.assertEqual(self.cart_item_y.promo_hash, promo_hash)
    #     print(f"Buy X Get Y CartItem saved: Modified Price: {self.cart_item_y.modified_price}")
    #     print("==================\n")

    def test_cart_checkout_process(self):
        # Test the full cart to checkout process
        print("Test cart checkout process:")
        checkout = Checkout.objects.create(user_hash='test_user_hash', cart=self.cart)
        self.assertGreater(checkout.cart.cartitem_set.count(), 0)
        print(f"Checkout items count: {checkout.cart.cartitem_set.count()}")
        print(f"Checkout item:")
        for item in checkout.cart.cartitem_set.all():
            print(f"  - Item {item}, price: {item.price}, modified prce: {item.modified_price}")
        self.assertGreater(checkout.final_price, 0)
        print(f"Checkout calculated:")
        print(f"  - Subtotal: {checkout.total_price}")
        print(f"  - Discount: {checkout.discount}")
        print(f"  - Subtotal after discount: {checkout.total_price - checkout.discount}")
        print(f"  - VAT: {checkout.vat}")
        print(f"  - Final Price: {checkout.final_price}")

        # Test creating an invoice
        invoice = Invoice.objects.create(checkout=checkout, invoice_number='INV123')
        self.assertEqual(invoice.status, 'pending')
        print(f"Invoice created: {invoice.invoice_number}, Status: {invoice.status}")
        print("==================\n")

if __name__ == '__main__':
    unittest.main()
