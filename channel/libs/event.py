from channel.models import Event
from rest_framework.exceptions import ValidationError

class EventLib:
    @staticmethod
    def list_events():
        return Event.objects.all()

    @staticmethod
    def get_event_by_hash(hash):
        try:
            return Event.objects.get(hash=hash)
        except Event.DoesNotExist:
            raise ValidationError("Event not found.")
