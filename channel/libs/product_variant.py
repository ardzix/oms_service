from channel.models import Product
from rest_framework.exceptions import ValidationError

class ProductVariantLib:
    @staticmethod
    def list_variants_by_parent_hash(hash):
        return Product.objects.filter(parent__hash=hash)
