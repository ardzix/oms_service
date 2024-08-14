# checkout/libs/checkout.py

from checkout.models import Checkout, Invoice
from rest_framework.exceptions import ValidationError
from checkout.serializers import CheckoutSerializer

class CheckoutLib:
    @staticmethod
    def create_checkout(data):
        serializer = CheckoutSerializer(data=data)
        if serializer.is_valid():
            return serializer.save()
        else:
            raise ValidationError(serializer.errors)

    @staticmethod
    def list_checkouts(user_hash):
        return Checkout.objects.filter(user_hash=user_hash)

    @staticmethod
    def get_checkout_detail(checkout_hash):
        try:
            checkout = Checkout.objects.get(hash=checkout_hash)
            return checkout
        except Checkout.DoesNotExist:
            raise ValidationError("Checkout not found")

    @staticmethod
    def update_checkout(instance, data):
        serializer = CheckoutSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            return serializer.save()
        else:
            raise ValidationError(serializer.errors)

    @staticmethod
    def delete_checkout(checkout_hash):
        try:
            checkout = Checkout.objects.get(hash=checkout_hash)
            checkout.delete()
        except Checkout.DoesNotExist:
            raise ValidationError("Checkout not found")
