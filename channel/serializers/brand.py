from rest_framework import serializers
from channel.models import Brand

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['hash', 'name', 'description', 'is_active']
