# checkout/serializers.py

# checkout/serializers.py

from rest_framework import serializers
from checkout.models import Checkout, Invoice
from cart.models import Cart
from cart.serializers import CartItemSerializer
from rest_framework.exceptions import ValidationError


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = [
            "hash",
            "user_hash",
            "cart",
            "total_price",
            "discount",
            "vat",
            "final_price",
            "created_at"
        ]
        read_only_fields = ["hash", "created_at"]

    def create(self, validated_data):
        try:
            cart = Cart.objects.get(hash=validated_data["cart"].hash)
        except Cart.DoesNotExist:
            raise ValidationError("Cart not found")
        return Checkout.objects.create(user_hash=validated_data["user_hash"], cart=cart)

    def update(self, instance, validated_data):
        instance.total_price = validated_data.get("total_price", instance.total_price)
        instance.discount = validated_data.get("discount", instance.discount)
        instance.vat = validated_data.get("vat", instance.vat)
        instance.final_price = validated_data.get("final_price", instance.final_price)
        instance.save()
        return instance

    def to_representation(self, instance):
        representaion = super().to_representation(instance)
        representaion["cart"] = instance.cart.hash
        return representaion


class CheckoutDetailSerializer(CheckoutSerializer):

    def to_representation(self, instance):
        representaion = super().to_representation(instance)
        representaion["items"] = CartItemSerializer(instance.cart.cart_items.all(), many=True).data
        representaion["invoice"] = InvoiceSerializer(instance.invoice).data if instance.invoice else None
        return representaion


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["invoice_number", "status", "created_at"]
