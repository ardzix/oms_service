import grpc
from django.conf import settings
from . import payment_pb2, payment_pb2_grpc

class PaymentClient:
    def __init__(self, host=settings.PAYMENT_SERVICE_HOST, port=settings.PAYMENT_SERVICE_PORT):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = payment_pb2_grpc.PaymentServiceStub(self.channel)

    def process_payment(self, user_id, amount, currency, payment_method, phone_number, ewallet_checkout_method, 
                        qr_type, qr_callback_url, invoice_number, agent, items):
        request = payment_pb2.ProcessPaymentRequest(
            user_id=user_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            phone_number=phone_number,
            ewallet_checkout_method=ewallet_checkout_method,
            qr_type=qr_type,
            qr_callback_url=qr_callback_url,
            invoice_number=invoice_number,
            agent=agent,
            items=[payment_pb2.Item(item_name=item['item_name'], quantity=item['quantity'], price=item['price']) for item in items]
        )
        return self.stub.ProcessPayment(request)

    def refund_payment(self, payment_id, amount):
        request = payment_pb2.RefundPaymentRequest(
            payment_id=payment_id,
            amount=amount
        )
        return self.stub.RefundPayment(request)

    def get_payment_status(self, payment_id):
        request = payment_pb2.GetPaymentStatusRequest(
            payment_id=payment_id
        )
        return self.stub.GetPaymentStatus(request)

    def get_payment_detail(self, payment_id):
        request = payment_pb2.GetPaymentDetailRequest(
            payment_id=payment_id
        )
        return self.stub.GetPaymentDetail(request)

    def list_payments(self, user_id, page=1, page_size=10):
        request = payment_pb2.ListPaymentsRequest(
            user_id=user_id,
            page=page,
            page_size=page_size
        )
        return self.stub.ListPayments(request)
