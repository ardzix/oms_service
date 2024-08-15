import pulsar
from django.core.management.base import BaseCommand
from checkout.pulsar.consumers import PaymentStatusUpdateListener
from django.conf import settings


class Command(BaseCommand):
    help = "Listen to multiple Pulsar topics and process messages."

    def handle(self, *args, **options):
        client = pulsar.Client(f'pulsar://{settings.PULSAR_HOST}:{settings.PULSAR_PORT}')
        listeners = [
            PaymentStatusUpdateListener(client),
            # Add more listeners here
        ]

        for listener in listeners:
            listener.start()
