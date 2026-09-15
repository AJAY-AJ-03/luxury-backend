from rest_framework import serializers
from products.models import Product
from products.serializers import ProductListSerializer
# pyrefly: ignore [missing-import]
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'subtotal', 'created_at', 'updated_at')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_items', 'total_price', 'created_at', 'updated_at')


class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_available=True).exists():
            raise serializers.ValidationError("Product does not exist or is unavailable.")
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, attrs):
        product_id = attrs.get('product_id')
        quantity = attrs.get('quantity')
        try:
            product = Product.objects.get(id=product_id)
            if product.stock < quantity:
                raise serializers.ValidationError({"quantity": f"Only {product.stock} items are in stock."})
        except Product.DoesNotExist:
            pass
        return attrs


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        if self.instance:
            product = self.instance.product
            if product.stock < quantity:
                raise serializers.ValidationError({"quantity": f"Only {product.stock} items are in stock."})
        return attrs
