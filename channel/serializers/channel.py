from rest_framework import serializers
from channel.models import Channel

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['hash', 'name', 'description', 'brand']

    def to_representation(self, instance):
        representaion = super().to_representation(instance)
        representaion['brand'] = instance.brand.hash
        return representaion