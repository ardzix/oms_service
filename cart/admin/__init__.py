from django.contrib import admin
from ..models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # Number of empty forms to display

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_hash', 'brand', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('user_hash', 'brand__name')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'price', 'promo_hash', 'modified_price')
    list_filter = ('cart',)
    search_fields = ('cart__user_hash', 'product__product_hash', 'promo_hash')
