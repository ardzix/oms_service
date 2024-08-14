# checkout/grpc/grpc_services.py

import grpc
import logging
from rest_framework.exceptions import ValidationError
from cart.models import Cart
from checkout.libs.checkout import CheckoutLib
from checkout.models import Checkout
from . import checkout_pb2, checkout_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CheckoutService(checkout_pb2_grpc.CheckoutServiceServicer):

    def CreateCheckout(self, request, context):
        logger.info(f"Received CreateCheckout request for cart_hash: {request.cart_hash}")
        try:
            cart = Cart.objects.get(hash=request.cart_hash)
        except Exception as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

        try:
            checkout_data = {
                'user_hash': request.user_hash,
                'cart': cart.pk,
            }
            checkout = CheckoutLib.create_checkout(checkout_data)
            return self._checkout_response(checkout)
        except ValidationError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

    def ListCheckouts(self, request, context):
        logger.info(f"Received ListCheckouts request for user_hash: {request.user_hash}")
        checkouts = CheckoutLib.list_checkouts(request.user_hash)
        response = checkout_pb2.ListCheckoutsResponse()
        for checkout in checkouts:
            response.checkouts.add().CopyFrom(self._checkout_response(checkout))
        return response

    def GetCheckoutDetail(self, request, context):
        logger.info(f"Received GetCheckoutDetail request for hash: {request.hash}")
        try:
            checkout, invoice = CheckoutLib.get_checkout_detail(request.hash)
            response = checkout_pb2.CheckoutDetailResponse()
            response.checkout.CopyFrom(self._checkout_response(checkout))
            if invoice:
                response.invoice.CopyFrom(self._invoice_response(invoice))
            return response
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def UpdateCheckout(self, request, context):
        logger.info(f"Received UpdateCheckout request for hash: {request.hash}")
        try:
            checkout = Checkout.objects.get(hash=request.hash)
            updated_checkout = CheckoutLib.update_checkout(checkout, {
                'total_price': request.total_price,
                'discount': request.discount,
                'vat': request.vat,
                'final_price': request.final_price,
            })
            return self._checkout_response(updated_checkout)
        except ValidationError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

    def DeleteCheckout(self, request, context):
        logger.info(f"Received DeleteCheckout request for hash: {request.hash}")
        try:
            CheckoutLib.delete_checkout(request.hash)
            return checkout_pb2.Empty()
        except ValidationError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def _checkout_response(self, checkout):
        return checkout_pb2.CheckoutResponse(
            hash=str(checkout.hash),
            user_hash=checkout.user_hash,
            cart_hash=str(checkout.cart.hash),
            total_price=float(checkout.total_price),
            discount=float(checkout.discount),
            vat=float(checkout.vat),
            final_price=float(checkout.final_price),
            created_at=str(checkout.created_at)
        )

    def _invoice_response(self, invoice):
        return checkout_pb2.InvoiceResponse(
            invoice_number=invoice.invoice_number,
            status=invoice.status,
            created_at=str(invoice.created_at)
        )
