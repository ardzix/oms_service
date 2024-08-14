from channel.models import Channel
from rest_framework.exceptions import ValidationError

class ChannelLib:
    @staticmethod
    def list_channels():
        return Channel.objects.all()

    @staticmethod
    def get_channel_by_hash(hash):
        try:
            return Channel.objects.get(hash=hash)
        except Channel.DoesNotExist:
            raise ValidationError("Channel not found.")
