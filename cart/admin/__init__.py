from django.contrib import admin
from ..models import Cart, CartItem, BuyXGetYPromo

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_hash', 'brand', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('user_hash', 'brand__name')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'price', 'promo_hash', 'modified_price', 'is_bogo', 'bogo_quantity', 'is_point_purchase', 'points_payable')
    list_filter = ('is_bogo', 'is_point_purchase')
    search_fields = ('cart__user_hash', 'product__product_hash', 'promo_hash')

@admin.register(BuyXGetYPromo)
class BuyXGetYPromoAdmin(admin.ModelAdmin):
    list_display = ('promo_hash', 'required_product', 'discounted_product', 'discounted_price')
    search_fields = ('promo_hash', 'required_product__product_hash', 'discounted_product__product_hash')
