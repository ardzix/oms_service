from rest_framework import viewsets
from rest_framework.response import Response
from channel.models import Brand
from channel.serializers.brand import BrandSerializer
from channel.libs.brand import BrandLib
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

class BrandViewSet(viewsets.ViewSet):
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        brands = BrandLib.list_brands()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)
