from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import Product
from .models import Cart, CartItem
from .serializers import (
    AddCartItemSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)


class CartView(APIView):
    """
    Retrieve the current user's cart. Creates one if it doesn't exist.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemAddView(APIView):
    """
    Add a product to the user's cart. If the product is already in the cart,
    increments the quantity (validating total requested against available stock).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        product = Product.objects.get(id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity
            if product.stock < new_quantity:
                return Response(
                    {"quantity": f"Only {product.stock} items are in stock. You already have {cart_item.quantity} in your cart."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class CartItemDetailView(APIView):
    """
    Update quantity or remove a specific product from the cart.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, product_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        serializer = UpdateCartItemSerializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        cart_item.quantity = serializer.validated_data['quantity']
        cart_item.save()

        return Response(CartSerializer(cart).data)

    def delete(self, request, product_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class CartClearView(APIView):
    """
    Clear all items in the user's cart.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)
