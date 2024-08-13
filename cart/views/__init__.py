from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from cart.models import Cart, CartItem
from channel.models import Brand, Product
from cart.serializers import CartSerializer, CartItemSerializer
from cart.libs.cart import CartLib
from cart.libs.cart_item import CartItemLib


class CartViewSet(viewsets.ViewSet):
    lookup_field = "hash"  # Specify that the lookup field is 'hash'

    @swagger_auto_schema(
        operation_description="Get or create a cart",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_hash": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User hash"
                ),
                "brand_hash": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Brand hash"
                ),
            },
            required=["user_hash", "brand_hash"],
        ),
        responses={200: CartSerializer(), 400: "Bad Request", 404: "Not Found"},
    )
    @action(detail=False, methods=["post"])
    def get_or_create_cart(self, request):
        brand = Brand.objects.filter(hash=request.data.get("brand_hash")).first()
        if not brand:
            return Response(
                {"detail": "Brand not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CartSerializer(
            data={
                "user_hash": request.data.get("user_hash"),
                "brand": brand.id,
            }
        )

        if serializer.is_valid():
            cart = serializer.save()
            cart_response = {
                "hash": str(cart.hash),
                "user_hash": cart.user_hash,
                "brand_hash": request.data.get("brand_hash"),
                "is_active": cart.is_active,
                "created_at": str(cart.created_at),
                "updated_at": str(cart.updated_at),
            }
            return Response(cart_response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Get cart detail",
        responses={200: CartSerializer(), 404: "Not Found"},
    )
    @action(detail=True, methods=["get"])
    def get_cart_detail(self, request, hash=None):
        try:
            cart = CartLib.get_cart_detail(hash)
            serializer = CartSerializer(cart)
            cart_response = serializer.data
            return Response(cart_response, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Add to cart",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "product_hash": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product/variant hash"
                ),
                "quantity": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Quantity"
                ),
            },
            required=["product_hash", "quantity"],
        ),
        responses={201: CartItemSerializer(), 400: "Bad Request", 404: "Not Found"},
    )
    @action(detail=True, methods=["post"])
    def add_to_cart(self, request, hash=None):
        try:
            cart = Cart.objects.get(hash=hash)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            product = Product.objects.get(
                Q(product_hash=request.data.get("product_hash"))
                | Q(variant_hash=request.data.get("product_hash"))
            )
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CartItemSerializer(
            data={
                "cart": cart.id,
                "product": product.id,
                "quantity": request.data.get("quantity"),
                "price": product.price,
            }
        )

        if serializer.is_valid():
            cart_item = serializer.save()
            cart_item_response = CartItemSerializer(cart_item).data
            return Response(cart_item_response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Apply promo to a cart item",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "promo_hash": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Promo hash"
                ),
            },
            required=["promo_hash"],
        ),
        responses={200: CartItemSerializer(), 400: "Bad Request", 404: "Not Found"},
    )
    @action(detail=True, methods=["post"])
    def apply_cart_item_promo(self, request, hash=None):
        try:
            cart_item = CartItem.objects.get(hash=hash)
        except CartItem.DoesNotExist:
            return Response(
                {"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CartItemSerializer(
            cart_item, data={"promo_hash": request.data.get("promo_hash")}, partial=True
        )
        if serializer.is_valid():
            cart_item = serializer.save()
            cart_item_response = CartItemSerializer(cart_item).data
            return Response(cart_item_response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Remove a cart item",
        responses={204: "No Content", 404: "Not Found"},
    )
    @action(detail=True, methods=["delete"])
    def remove_cart_item(self, request, hash=None):
        try:
            CartItemLib.remove_cart_item(hash)
            return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Clear all items in the cart",
        responses={204: "No Content", 404: "Not Found"},
    )
    @action(detail=True, methods=["delete"])
    def clear_cart(self, request, hash=None):
        try:
            cart = Cart.objects.get(hash=hash)
            CartLib.clear_cart(cart)
            return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND
            )
