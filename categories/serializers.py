from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'image',
            'is_active',
            'product_count',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at', 'product_count')

    def get_product_count(self, obj):
        return obj.products.filter(is_available=True).count()

    def validate_name(self, value):
        return value.strip()


class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list endpoints."""

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'is_active')
