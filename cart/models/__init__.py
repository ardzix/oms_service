import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from channel.models import Product, Brand


class Cart(models.Model):
    user_hash = models.CharField(max_length=255)
    hash = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon_code = models.CharField(max_length=64, null=True, blank=True)
    promo_hash = models.CharField(max_length=255, null=True, blank=True)
    available_promos = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cart {self.id} for user {self.user_hash}"

    def get_available_promos(self):
        # Convert the comma-separated string to a list
        return self.available_promos.split(',') if self.available_promos else []

    def set_available_promos(self, promos):
        # Convert the list to a comma-separated string
        self.available_promos = ','.join(promos)

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

class CartItem(models.Model):
    hash = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_code = models.CharField(max_length=64, null=True, blank=True)
    promo_hash = models.CharField(max_length=255, null=True, blank=True)
    available_promos = models.TextField(blank=True, null=True)
    modified_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.product} in cart {self.cart.id}"

    def get_available_promos(self):
        # Convert the comma-separated string to a list
        return self.available_promos.split(',') if self.available_promos else []

    def set_available_promos(self, promos):
        # Convert the list to a comma-separated string
        self.available_promos = ','.join(promos)
    
    @property
    def item_name(self):
        return self.product.__str__()

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
