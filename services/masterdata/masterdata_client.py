import grpc
from django.conf import settings
from . import masterdata_pb2, masterdata_pb2_grpc

class MasterDataClient:
    def __init__(self, host=settings.MASTERDATA_SERVICE_HOST, port=settings.MASTERDATA_SERVICE_PORT):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = masterdata_pb2_grpc.MasterDataServiceStub(self.channel)

    def get_product(self, product_hash):
        request = masterdata_pb2.GetProductRequest(hash=product_hash)
        return self.stub.GetProduct(request)

    def list_products(self):
        request = masterdata_pb2.Empty()
        return self.stub.ListProducts(request)
    
    def get_vat_rate(self):
        return 0.11

    # Add other methods as needed
