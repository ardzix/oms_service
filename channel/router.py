from rest_framework.routers import DefaultRouter
from .views.brand import BrandViewSet
from .views.channel import ChannelViewSet
from .views.event import EventViewSet
from .views.product import ProductViewSet
from .views.product_variant import ProductVariantViewSet


router = DefaultRouter()
router.register("brand", BrandViewSet, basename="brand")
router.register("channel", ChannelViewSet, basename="channel")
router.register("event", EventViewSet, basename="event")
router.register("product", ProductViewSet, basename="product")
router.register("product_variant", ProductVariantViewSet, basename="product_variant")