# server.py
import os
import grpc
from concurrent import futures
import time
import logging

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oms.settings')

import django
django.setup()

from django.conf import settings
from cart.grpc import cart_pb2_grpc
from cart.grpc.grpc_services import CartService
from channel.grpc import oms_channel_pb2_grpc
from channel.grpc.grpc_services import ChannelService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    cart_pb2_grpc.add_CartServiceServicer_to_server(CartService(), server)
    oms_channel_pb2_grpc.add_ChannelServiceServicer_to_server(ChannelService(), server)

    # Listen on two different ports
    server.add_insecure_port(f'[::]:{settings.OMS_CART_SERVICE_PORT}')
    server.add_insecure_port(f'[::]:{settings.OMS_CHANNEL_SERVICE_PORT}')

    server.start()
    logger.info(f'gRPC servers running on ports {settings.OMS_CART_SERVICE_PORT} and {settings.OMS_CHANNEL_SERVICE_PORT}...')
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
