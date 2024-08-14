from rest_framework import viewsets
from rest_framework.response import Response
from channel.serializers.product import ProductSerializer
from channel.libs.product import ProductLib
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


class ProductViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="List Brand Channel Products",
        manual_parameters=[
            openapi.Parameter(
                "brand_hash", openapi.IN_QUERY, description="Brand hash", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                "channel_hash", openapi.IN_QUERY, description="Channel hash", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                "event_hash", openapi.IN_QUERY, description="Event hash (optional)", type=openapi.TYPE_STRING, required=False
            ),
        ],
        responses={200: ProductSerializer(many=True), 400: "Bad Request", 404: "Not Found"},
    )
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        channel_hash = request.query_params.get('channel_hash')
        brand_hash = request.query_params.get('brand_hash')
        event_hash = request.query_params.get('event_hash', None)

        products = ProductLib.list_products(channel_hash, brand_hash, event_hash)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
