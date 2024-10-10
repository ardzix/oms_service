import grpc
from django.conf import settings
from . import promo_pb2, promo_pb2_grpc

class PromoClient:
    def __init__(self, host=settings.PPL_PROMO_SERVICE_HOST, port=settings.PPL_PROMO_SERVICE_PORT):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = promo_pb2_grpc.PromoServiceStub(self.channel)

    def check_item_promo(self, product_hash, coupon_code=None):
        """Check if a single product is eligible for any promotions."""
        request = promo_pb2.CheckItemPromoRequest(
            product_hash=product_hash,
            coupon_code=coupon_code or ""
        )
        return self.stub.CheckItemPromo(request)

    def check_items_promos(self, items, subtotal, coupon_code=None):
        """Check if a list of items is eligible for bundle or threshold promos."""
        request = promo_pb2.CheckItemsPromosRequest(
            items=items,
            subtotal=subtotal,
            coupon_code=coupon_code or ""
        )
        return self.stub.CheckItemsPromos(request)

    def get_promo_by_hash(self, promo_hash):
        """Retrieve a promo by its hash."""
        request = promo_pb2.PromoByHashRequest(promo_hash=promo_hash)
        return self.stub.GetPromoByHash(request)

    def list_promos(self, page=1, page_size=10, promo_type=None, brand_hash=None, channel_hash=None, event_hash=None, active=None):
        """List promos with pagination and optional filtering."""
        request = promo_pb2.ListPromosRequest(
            page=page,
            page_size=page_size,
            promo_type=promo_type or "",
            brand_hash=brand_hash or "",
            channel_hash=channel_hash or "",
            event_hash=event_hash or "",
            active=active if active is not None else False
        )
        return self.stub.ListPromos(request)

    def create_discount_promo(self, name, description, start_date, end_date, active, brand_hash, channel_hash, discount_type, discount_value, product_hash, coupon=None, usage_limits=None):
        """Create a discount promo."""
        request = promo_pb2.CreateDiscountPromoRequest(
            name=name,
            description=description,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            active=active,
            brand_hash=brand_hash,
            channel_hash=channel_hash,
            discount_promo=promo_pb2.DiscountPromoDetails(
                discount_type=discount_type,
                discount_value=discount_value,
                product_hash=product_hash
            ),
            coupon=coupon or promo_pb2.CouponDetails(),
            usage_limits=usage_limits or promo_pb2.PromoUsageLimits()
        )
        return self.stub.CreateDiscountPromo(request)

    def create_bundle_promo(self, name, description, start_date, end_date, active, brand_hash, channel_hash, bundle_promo, coupon=None, usage_limits=None):
        """Create a bundle promo."""
        request = promo_pb2.CreateBundlePromoRequest(
            name=name,
            description=description,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            active=active,
            brand_hash=brand_hash,
            channel_hash=channel_hash,
            bundle_promo=bundle_promo,
            coupon=coupon or promo_pb2.CouponDetails(),
            usage_limits=usage_limits or promo_pb2.PromoUsageLimits()
        )
        return self.stub.CreateBundlePromo(request)

    def update_discount_promo(self, promo_hash, name, description, start_date, end_date, active, brand_hash, channel_hash, discount_type, discount_value, product_hash, coupon=None, usage_limits=None):
        """Update a discount promo."""
        request = promo_pb2.UpdateDiscountPromoRequest(
            promo_hash=promo_hash,
            name=name,
            description=description,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            active=active,
            brand_hash=brand_hash,
            channel_hash=channel_hash,
            discount_promo=promo_pb2.DiscountPromoDetails(
                discount_type=discount_type,
                discount_value=discount_value,
                product_hash=product_hash
            ),
            coupon=coupon or promo_pb2.CouponDetails(),
            usage_limits=usage_limits or promo_pb2.PromoUsageLimits()
        )
        return self.stub.UpdateDiscountPromo(request)

    def delete_promo(self, promo_hash):
        """Delete a promo by its hash."""
        request = promo_pb2.DeletePromoRequest(promo_hash=promo_hash)
        return self.stub.DeletePromo(request)
