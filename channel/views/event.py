from rest_framework import viewsets
from rest_framework.response import Response
from channel.serializers.event import EventSerializer
from channel.libs.event import EventLib
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

class EventViewSet(viewsets.ViewSet):
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        events = EventLib.list_events()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
