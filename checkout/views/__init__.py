# checkout/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from checkout.serializers import (
    CheckoutSerializer,
    CheckoutDetailSerializer,
    InvoiceSerializer,
)
from checkout.libs.checkout import CheckoutLib
from cart.models import Cart
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CheckoutViewSet(viewsets.GenericViewSet):
    lookup_field = "hash"  # Specify that the lookup field is 'hash'

    @swagger_auto_schema(
        operation_description="Add to cart",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_hash": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User hash"
                ),
                "cart_hash": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Cart hash"
                ),
            },
            required=["product_hash", "quantity"],
        ),
        responses={
            201: CheckoutDetailSerializer(),
            400: "Bad Request",
            404: "Not Found",
        },
    )
    def create(self, request):
        try:
            cart = Cart.objects.get(hash=request.data.get("cart_hash"))
            checkout = CheckoutLib.create_checkout(
                {
                    "cart": cart.pk,
                    "user_hash": request.data.get("user_hash"),
                }
            )
            return Response(
                CheckoutDetailSerializer(checkout).data, status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="List Brand Channel Products",
        manual_parameters=[
            openapi.Parameter(
                "user_hash",
                openapi.IN_QUERY,
                description="User hash",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: CheckoutSerializer(many=True),
            400: "Bad Request",
            404: "Not Found",
        },
    )
    def list(self, request):
        user_hash = request.query_params.get("user_hash")
        checkouts = CheckoutLib.list_checkouts(user_hash)
        serializer = CheckoutSerializer(checkouts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, hash=None):
        try:
            checkout = CheckoutLib.get_checkout_detail(hash)
            checkout_data = CheckoutDetailSerializer(checkout).data
            return Response(checkout_data)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
