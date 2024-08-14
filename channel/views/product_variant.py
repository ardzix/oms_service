from rest_framework import viewsets
from rest_framework.response import Response
from channel.serializers.product_variant import ProductVariantSerializer
from channel.libs.product_variant import ProductVariantLib
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

class ProductVariantViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="List Variants based on Product hash",
        manual_parameters=[
            openapi.Parameter(
                "parent_hash", openapi.IN_QUERY, description="Parent Hash", type=openapi.TYPE_STRING, required=True
            ),
        ],
        responses={200: ProductVariantSerializer(many=True), 400: "Bad Request", 404: "Not Found"},
    )
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        parent_hash = request.query_params.get('parent_hash')
        variants = ProductVariantLib.list_variants_by_parent_hash(parent_hash)
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)
