import grpc
import logging
from rest_framework import serializers
from channel.models import Product
from google.protobuf.json_format import MessageToDict
from services.catalogue.catalogue_client import CatalogueClient

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class ProductVariantSerializer(serializers.ModelSerializer):
    parent_hash = serializers.CharField(source='parent.hash', allow_null=True, required=False)

    class Meta:
        model = Product
        fields = ['variant_hash', 'parent_hash', 'channel', 'event', 'brand', 'available', 'price', 'is_valid', 'hash']

    def to_representation(self, instance):
        representaion = super().to_representation(instance)
        representaion['brand'] = instance.brand.hash
        representaion['channel'] = instance.channel.hash
        representaion['event'] = instance.event.hash if instance.event else None

        catalogue = CatalogueClient()
        try:
            variant_response = catalogue.get_product_variant(instance.variant_hash)
            variant_details = MessageToDict(variant_response)
            representaion['variant_details'] = variant_details
        except grpc.RpcError as e:
            # Handle the gRPC error here
            error_code = e.code()
            error_details = e.details()
            # Log the error or handle it according to your needs
            logging.warning(f"gRPC call catalogue.get_product_varian with hash {instance.variant_hash} failed with error code: {error_code}, details: {error_details}")

        return representaion