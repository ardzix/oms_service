# tasks.py
from django_q.tasks import async_task
from services.payment.payment_client import PaymentClient
from checkout.models import Invoice

def send_invoice_to_payment_service_task(invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        items = [{"item_name": item.item_name, "quantity": item.quantity, "price": item.price} for item in invoice.checkout.cart_items]
        payment_client = PaymentClient()
        payment_client.process_payment(
            amount=invoice.checkout.final_price,
            currency="IDR",
            payment_method=invoice.payment_method,
            qr_type="DYNAMIC",
            user_id=invoice.checkout.user_hash,
            phone_number='08581111111111',
            ewallet_checkout_method='ONE_TIME_PAYMENT',
            invoice_number=invoice.invoice_number,
            agent='OMS',
            qr_callback_url="https://femaledaily.net/payment_callback",
            items=items
        )
    except Invoice.DoesNotExist:
        # Handle exception (e.g., log it or pass)
        pass
