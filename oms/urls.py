from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from cart.views import CartViewSet
from django.conf import settings
from channel.router import router as channel_router
from checkout.views import CheckoutViewSet

# Router for the REST API
cart_router = DefaultRouter()
cart_router.register(r'carts', CartViewSet, basename='cart')
checkout_router = DefaultRouter()
checkout_router.register(r'checkouts', CheckoutViewSet, basename='checkout')

# Swagger/OpenAPI configuration
schema_view = get_schema_view(
    openapi.Info(
        title="OMS API",
        default_version='v1',
        description="API documentation for the Order Management System",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=settings.BASE_URL,
)

urlpatterns = [
    path(f'{settings.URL_PREFIX}api/channels/', include(channel_router.urls)),
    path(f'{settings.URL_PREFIX}api/', include(checkout_router.urls)),
    path(f'{settings.URL_PREFIX}api/', include(cart_router.urls)),
    path(f'{settings.URL_PREFIX}admin/', admin.site.urls),
    path(f'{settings.URL_PREFIX}api-docs/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(
        f"{settings.URL_PREFIX}swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(f"{settings.URL_PREFIX}redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
