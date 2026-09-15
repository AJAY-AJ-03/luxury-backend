from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    effective_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'category_name',
            'category_slug',
            'name',
            'slug',
            'description',
            'price',
            'discount_price',
            'effective_price',
            'stock',
            'image',
            'is_available',
            'sku',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'slug',
            'category_name',
            'category_slug',
            'effective_price',
            'created_at',
            'updated_at',
        )

    def validate_name(self, value):
        return value.strip()

    def validate_sku(self, value):
        return value.strip().upper()

    def validate_category(self, value):
        if not value.is_active:
            raise serializers.ValidationError('Cannot assign product to an inactive category.')
        return value

    def validate(self, attrs):
        price = attrs.get('price', getattr(self.instance, 'price', None))
        discount_price = attrs.get(
            'discount_price',
            getattr(self.instance, 'discount_price', None),
        )
        stock = attrs.get('stock', getattr(self.instance, 'stock', None))

        if discount_price is not None and price is not None:
            if discount_price >= price:
                raise serializers.ValidationError(
                    {'discount_price': 'Discount price must be less than regular price.'}
                )

        if stock is not None and stock == 0:
            attrs['is_available'] = attrs.get('is_available', False)

        return attrs


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    effective_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'category_name',
            'name',
            'slug',
            'price',
            'discount_price',
            'effective_price',
            'stock',
            'image',
            'is_available',
            'sku',
            'created_at',
        )
        read_only_fields = fields
