from channel.models import Product
from rest_framework.exceptions import ValidationError

class ProductLib:
    @staticmethod
    def list_products(channel_hash, brand_hash, event_hash=None):
        products = Product.objects.filter(channel__hash=channel_hash, brand__hash=brand_hash, parent__isnull=True)
        if event_hash and event_hash != 'all':
            if event_hash == 'global':
                products = products.filter(event__hash__isnull=True)
            else:
                products = products.filter(event__hash=event_hash)
        return products

    @staticmethod
    def get_product_by_hash(hash):
        try:
            return Product.objects.get(hash=hash)
        except Product.DoesNotExist:
            raise ValidationError("Product not found.")

    @staticmethod
    def delete_product_by_hash(hash):
        try:
            return Product.objects.get(hash=hash).delete()
        except Product.DoesNotExist:
            raise ValidationError("Product not found.")
