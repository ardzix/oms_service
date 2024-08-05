import grpc
from django.conf import settings
from . import promo_pb2, promo_pb2_grpc

class PromoClient:
    def __init__(self, host=settings.PPL_PROMO_SERVICE_HOST, port=settings.PPL_PROMO_SERVICE_PORT):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = promo_pb2_grpc.PromoServiceStub(self.channel)

    def get_product_promos(self, product_hash):
        request = promo_pb2.ProductPromoRequest(product_hash=product_hash)
        return self.stub.GetProductPromos(request)

    def check_threshold_promo(self, subtotal):
        request = promo_pb2.ThresholdPromoRequest(subtotal=subtotal)
        return self.stub.CheckThresholdPromo(request)

    def get_promo_by_hash(self, promo_hash):
        request = promo_pb2.PromoByHashRequest(promo_hash=promo_hash)
        return self.stub.GetPromoByHash(request)
