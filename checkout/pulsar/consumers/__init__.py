import json
import logging
from checkout.libs.pulsar_listener import PulsarListener
from checkout.models import Invoice

logger = logging.getLogger(__name__)

class PaymentStatusUpdateListener(PulsarListener):
    """
    Listener for payment status updates to update the Invoice model.
    """
    topic = 'persistent://public/default/payment-status_update'
    subscription_name = 'invoice-update-subscription'

    def process_message(self, msg):
        data = json.loads(msg.data().decode('utf-8'))
        transaction_id = data.get('transaction_id')
        status = data.get('status')
        if transaction_id and status:
            try:
                invoice = Invoice.objects.get(invoice_number=transaction_id)
                invoice.status = Invoice.PAID if status == 'settlement' else Invoice.PENDING
                invoice.save()
                logger.info(f"Updated invoice {transaction_id} to status {status}.")
            except Invoice.DoesNotExist:
                logger.error(f"Invoice with transaction ID {transaction_id} not found.")