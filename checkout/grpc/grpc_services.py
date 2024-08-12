import grpc
from concurrent import futures
import logging
from django.core.exceptions import ObjectDoesNotExist
from checkout.models import Checkout, Invoice
from cart.models import Cart
from . import checkout_pb2, checkout_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CheckoutService(checkout_pb2_grpc.CheckoutServiceServicer):

    def CreateCheckout(self, request, context):
        logger.info(f"Received CreateCheckout request for cart_hash: {request.cart_hash}")
        try:
            cart = Cart.objects.get(hash=request.cart_hash)
            checkout = Checkout.objects.create(
                user_hash=request.user_hash,
                cart=cart
            )
            return self._checkout_response(checkout)
        except Cart.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Cart not found")

    def ListCheckouts(self, request, context):
        logger.info(f"Received ListCheckouts request for user_hash: {request.user_hash}")
        checkouts = Checkout.objects.filter(user_hash=request.user_hash)
        response = checkout_pb2.ListCheckoutsResponse()
        for checkout in checkouts:
            response.checkouts.append(self._checkout_response(checkout))
        return response

    def GetCheckoutDetail(self, request, context):
        logger.info(f"Received GetCheckoutDetail request for hash: {request.hash}")
        try:
            checkout = Checkout.objects.get(hash=request.hash)
            response = checkout_pb2.CheckoutDetailResponse()
            response.checkout.CopyFrom(self._checkout_response(checkout))
            try:
                invoice = Invoice.objects.get(checkout=checkout)
                response.invoice.invoice_number = invoice.invoice_number
                response.invoice.status = invoice.status
                response.invoice.created_at = str(invoice.created_at)
            except Invoice.DoesNotExist:
                pass
            return response
        except Checkout.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Checkout not found")

    def UpdateCheckout(self, request, context):
        logger.info(f"Received UpdateCheckout request for hash: {request.hash}")
        try:
            checkout = Checkout.objects.get(hash=request.hash)
            checkout.total_price = request.total_price
            checkout.discount = request.discount
            checkout.vat = request.vat
            checkout.final_price = request.final_price
            checkout.save()
            return self._checkout_response(checkout)
        except Checkout.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Checkout not found")

    def DeleteCheckout(self, request, context):
        logger.info(f"Received DeleteCheckout request for hash: {request.hash}")
        try:
            checkout = Checkout.objects.get(hash=request.hash)
            checkout.delete()
            return checkout_pb2.Empty()
        except Checkout.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Checkout not found")

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