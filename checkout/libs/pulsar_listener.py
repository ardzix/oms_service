import logging
from django.core.management.base import BaseCommand
from checkout.models import Invoice  # Replace 'myapp' with your app name

logger = logging.getLogger(__name__)

class PulsarListener:
    """
    Base class for creating a Pulsar listener.
    """
    topic = ''
    subscription_name = ''
    
    def __init__(self, client):
        self.client = client
        self.consumer = self.client.subscribe(
            self.topic,
            self.subscription_name
        )
    
    def process_message(self, msg):
        """
        Process the received message. Should be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    def start(self):
        logger.info(f"Listening to {self.topic} on subscription {self.subscription_name}")
        try:
            while True:
                msg = self.consumer.receive()
                logger.info(f"Received message: {msg.data().decode('utf-8')}")
                self.process_message(msg)
                self.consumer.acknowledge(msg)
        except KeyboardInterrupt:
            logger.info(f"Stopping listener for {self.topic}")
        finally:
            self.client.close()