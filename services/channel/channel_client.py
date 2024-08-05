import grpc
from django.conf import settings
from . import channel_pb2, channel_pb2_grpc

class ChannelClient:
    def __init__(self, host=settings.MD_CHANNEL_SERVICE_HOST, port=settings.MD_CHANNEL_SERVICE_PORT):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = channel_pb2_grpc.ChannelServiceStub(self.channel)

    # Brand Operations
    def get_brand(self, brand_hash):
        request = channel_pb2.GetBrandRequest(hash=brand_hash)
        return self.stub.GetBrand(request)

    def create_brand(self, name, description, is_active):
        request = channel_pb2.CreateBrandRequest(
            name=name,
            description=description,
            is_active=is_active
        )
        return self.stub.CreateBrand(request)

    def update_brand(self, brand_hash, name, description, is_active):
        request = channel_pb2.UpdateBrandRequest(
            hash=brand_hash,
            name=name,
            description=description,
            is_active=is_active
        )
        return self.stub.UpdateBrand(request)

    def delete_brand(self, brand_hash):
        request = channel_pb2.DeleteBrandRequest(hash=brand_hash)
        return self.stub.DeleteBrand(request)

    def list_brands(self):
        request = channel_pb2.Empty()
        return self.stub.ListBrands(request)

    # Channel Operations
    def get_channel(self, channel_hash):
        request = channel_pb2.GetChannelRequest(hash=channel_hash)
        return self.stub.GetChannel(request)

    def create_channel(self, name, description, brand_hash):
        request = channel_pb2.CreateChannelRequest(
            name=name,
            description=description,
            brand_hash=brand_hash
        )
        return self.stub.CreateChannel(request)

    def update_channel(self, channel_hash, name, description, brand_hash):
        request = channel_pb2.UpdateChannelRequest(
            hash=channel_hash,
            name=name,
            description=description,
            brand_hash=brand_hash
        )
        return self.stub.UpdateChannel(request)

    def delete_channel(self, channel_hash):
        request = channel_pb2.DeleteChannelRequest(hash=channel_hash)
        return self.stub.DeleteChannel(request)

    def list_channels(self):
        request = channel_pb2.Empty()
        return self.stub.ListChannels(request)

    # Event Operations
    def get_event(self, event_hash):
        request = channel_pb2.GetEventRequest(hash=event_hash)
        return self.stub.GetEvent(request)

    def create_event(self, name, description, start_date, end_date, channel_hash, brand_hashes):
        request = channel_pb2.CreateEventRequest(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            channel_hash=channel_hash,
            brand_hashes=brand_hashes
        )
        return self.stub.CreateEvent(request)

    def update_event(self, event_hash, name, description, start_date, end_date, channel_hash, brand_hashes):
        request = channel_pb2.UpdateEventRequest(
            hash=event_hash,
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            channel_hash=channel_hash,
            brand_hashes=brand_hashes
        )
        return self.stub.UpdateEvent(request)

    def delete_event(self, event_hash):
        request = channel_pb2.DeleteEventRequest(hash=event_hash)
        return self.stub.DeleteEvent(request)

    def list_events(self):
        request = channel_pb2.Empty()
        return self.stub.ListEvents(request)

    # Event-Brand Operations
    def add_brand_to_event(self, event_hash, brand_hash):
        request = channel_pb2.AddBrandToEventRequest(
            event_hash=event_hash,
            brand_hash=brand_hash
        )
        return self.stub.AddBrandToEvent(request)

    def remove_brand_from_event(self, event_hash, brand_hash):
        request = channel_pb2.RemoveBrandFromEventRequest(
            event_hash=event_hash,
            brand_hash=brand_hash
        )
        return self.stub.RemoveBrandFromEvent(request)

    def set_brands_for_event(self, event_hash, brand_hashes):
        request = channel_pb2.SetBrandsForEventRequest(
            event_hash=event_hash,
            brand_hashes=brand_hashes
        )
        return self.stub.SetBrandsForEvent(request)
