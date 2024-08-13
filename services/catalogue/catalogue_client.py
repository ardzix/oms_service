import grpc
from django.conf import settings
from . import catalogue_pb2, catalogue_pb2_grpc

class CatalogueClient:
    def __init__(self, host=settings.MD_CATALOGUE_SERVICE_HOST, port=settings.MD_CATALOGUE_SERVICE_PORT):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = catalogue_pb2_grpc.CatalogueServiceStub(self.channel)

    def get_product(self, product_hash):
        request = catalogue_pb2.GetProductRequest(hash=product_hash)
        return self.stub.GetProduct(request)

    def list_products(self):
        request = catalogue_pb2.Empty()
        return self.stub.ListProducts(request)

    def get_product_variant(self, variant_hash):
        request = catalogue_pb2.GetProductVariantRequest(hash=variant_hash)
        return self.stub.GetProductVariant(request)

    def list_product_variants(self, product_hash):
        request = catalogue_pb2.ListProductVariantsRequest(hash=product_hash)
        return self.stub.ListProductVariants(request)
    
    def get_vat_rate(self):
        return 0.11