from channel.models import Brand
from rest_framework.exceptions import ValidationError

class BrandLib:
    @staticmethod
    def list_brands():
        return Brand.objects.all()

    @staticmethod
    def get_brand_by_hash(hash):
        try:
            return Brand.objects.get(hash=hash)
        except Brand.DoesNotExist:
            raise ValidationError("Brand not found.")
