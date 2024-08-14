from rest_framework import viewsets
from rest_framework.response import Response
from channel.serializers.channel import ChannelSerializer
from channel.libs.channel import ChannelLib
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

class ChannelViewSet(viewsets.ViewSet):
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        channels = ChannelLib.list_channels()
        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data)
