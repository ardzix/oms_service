import grpc
import logging
from rest_framework import serializers
from channel.models import Product
from google.protobuf.json_format import MessageToDict
from services.catalogue.catalogue_client import CatalogueClient

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_hash', 'channel', 'event', 'brand', 'available', 'price', 'is_valid', 'hash']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['brand'] = instance.brand.hash
        representation['channel'] = instance.channel.hash
        representation['event'] = instance.event.hash if instance.event else None

        catalogue = CatalogueClient()
        try:
            product_response = catalogue.get_product(instance.product_hash)
            product_details = MessageToDict(product_response)

            if 'variants' in product_details:
                product_details.pop('variants')

            representation['product_details'] = product_details

        except grpc.RpcError as e:
            # Handle the gRPC error here
            error_code = e.code()
            error_details = e.details()
            # Log the error or handle it according to your needs
            logging.warning(f"gRPC call catalogue.get_product with hash {instance.product_hash} failed with error code: {error_code}, details: {error_details}")

        return representation