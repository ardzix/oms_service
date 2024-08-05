import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from google.protobuf.json_format import MessageToDict
from services.catalogue.catalogue_client import CatalogueClient
from services.promo.promo_client import PromoClient
from channel.models import Product, Brand


class Cart(models.Model):
    user_hash = models.CharField(max_length=255, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hash = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)

    def __str__(self):
        return f"Cart {self.id} for user {self.user_hash}"

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

class BuyXGetYPromo(models.Model):
    promo_hash = models.CharField(max_length=255)
    required_product = models.ForeignKey(Product, related_name='required_product', on_delete=models.CASCADE)
    discounted_product = models.ForeignKey(Product, related_name='discounted_product', on_delete=models.CASCADE)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Buy {self.required_product.product_hash} Get {self.discounted_product.product_hash}"

    class Meta:
        verbose_name = _("Buy X Get Y Promo")
        verbose_name_plural = _("Buy X Get Y Promos")

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_hash = models.CharField(max_length=255, null=True, blank=True)
    modified_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_bogo = models.BooleanField(default=False)
    bogo_quantity = models.IntegerField(null=True, blank=True, default=0)
    is_point_purchase = models.BooleanField(default=False)
    points_payable = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Product {self.product.product_hash} in cart {self.cart.id}"

    def save(self, *args, **kwargs):
        self.price = self.product.price  # Fetching base price from master data
        
        promo_client = PromoClient()

        if self.promo_hash:
            promo_response = promo_client.get_promo_by_hash(self.promo_hash)

            if promo_response and promo_response.active:
                # Handle discount promo
                if promo_response.discount_promos:
                    doscount_promo=promo_response.discount_promos[0]
                    self.modified_price = doscount_promo.final_price

                # Handle BOGO promo
                if promo_response.bogo_promos and self.quantity >= 2:
                    self.is_bogo = True
                    self.bogo_quantity = self.quantity // 2
                    self.modified_price = (self.quantity - self.bogo_quantity) * self.price

                # Handle point purchase promo
                if promo_response.point_purchase_promos:
                    self.is_point_purchase = True
                    self.points_payable = promo_response.points_required
            else:
                raise ValueError("Invalid or inactive promo hash")
        else:
            # Check if this product is a "Y" product in a Buy X Get Y promo
            buy_x_get_y_promo = BuyXGetYPromo.objects.filter(discounted_product=self.product).first()
            if buy_x_get_y_promo:
                self.modified_price = buy_x_get_y_promo.discounted_price
                self.promo_hash = buy_x_get_y_promo.promo_hash
            else:
                self.modified_price = self.price

        
        product_promo_response = promo_client.get_product_promos(self.product.product_hash)
        if product_promo_response:
            buy_x_get_y_promos_list = [MessageToDict(promo) for promo in product_promo_response.buy_x_get_y_promos]
            for buy_x_get_y in buy_x_get_y_promos_list:
                BuyXGetYPromo.objects.create(
                    promo_hash=buy_x_get_y.get('promoHash'),
                    required_product=self.product,
                    discounted_product=Product.objects.get(product_hash=buy_x_get_y.get('discountedProductHash')),
                    discounted_price=buy_x_get_y.get('discountedPrice')
                )

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
