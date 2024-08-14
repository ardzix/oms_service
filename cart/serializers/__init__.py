from rest_framework import serializers
from cart.models import Cart, CartItem
from channel.models import Product, Brand
from rest_framework.exceptions import ValidationError
from google.protobuf.json_format import MessageToDict
from services.catalogue.catalogue_client import CatalogueClient


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'product', 'cart', 'quantity', 'price', 'promo_hash',
            'modified_price', 'is_bogo', 'bogo_quantity', 'is_point_purchase', 'points_payable', 'hash'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        catalogue = CatalogueClient()
        product_hash = instance.product.get_product_hash()
        product_response = catalogue.get_product(product_hash)
        product_details = MessageToDict(product_response)
        if 'variants' in product_details:
            product_details.pop('variants')

        variant_details = None
        if instance.product.variant_hash:
            variant_response = catalogue.get_product_variant(instance.product.variant_hash)
            variant_details = MessageToDict(variant_response)

        representation['product'] = {
            'type': 'product' if instance.product.product_hash else 'variant',
            'hash': instance.product.product_hash if instance.product.product_hash else instance.product.variant_hash,
            'product_details': product_details,
            'variant_details': variant_details
        }
        representation['cart'] = instance.cart.hash
        return representation

    def create(self, validated_data):
        # Create or update a CartItem
        cart_item, created = CartItem.objects.get_or_create(
            cart=validated_data['cart'],
            product=validated_data['product'],
            defaults={
                'quantity': validated_data['quantity'],
                'price': validated_data['price'],
            }
        )
        
        if not created:
            cart_item.quantity += validated_data['quantity']
            cart_item.save()

        return cart_item

    def update(self, instance, validated_data):
        # Update an existing CartItem
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.promo_hash = validated_data.get('promo_hash', instance.promo_hash)
        instance.save()

        return instance


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'user_hash', 'brand', 'is_active', 'created_at', 'updated_at', 'cart_items', 'hash'
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['brand'] = instance.brand.hash if instance.brand else None
        return representation

    def validate(self, data):
        # Ensure that the brand exists
        brand = data.get('brand')
        if not brand or not Brand.objects.filter(hash=brand.hash).exists():
            raise ValidationError("Brand does not exist.")
        
        return data

    def create(self, validated_data):
        # Create or get a Cart
        cart, created = Cart.objects.get_or_create(
            user_hash=validated_data['user_hash'],
            brand=validated_data['brand'],
            is_active=True,
        )
        return cart

    def update(self, instance, validated_data):
        # Update an existing Cart
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        return instance
