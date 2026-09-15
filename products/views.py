from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from core.permissions import IsAdminOrReadOnly

from .models import Product
from .serializers import ProductListSerializer, ProductSerializer


class ProductPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD API for products with search, filters, and pagination.
    Public: list and retrieve available products.
    Staff: full create, update, delete.
    """

    queryset = Product.objects.select_related('category')
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ProductPagination
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'category__slug', 'is_available']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['created_at', 'price', 'name', 'stock']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user and self.request.user.is_staff:
            return qs

        # Public users only see available products from active categories
        return qs.filter(is_available=True, category__is_active=True)
