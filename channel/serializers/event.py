from rest_framework import serializers
from channel.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['hash', 'name', 'description', 'start_date', 'end_date', 'channel', 'brand']

    def to_representation(self, instance):
        representaion = super().to_representation(instance)
        representaion['brand'] = instance.brand.hash
        representaion['channel'] = instance.channel.hash
        return representaion