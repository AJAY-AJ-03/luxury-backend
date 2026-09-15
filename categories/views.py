from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from core.permissions import IsAdminOrReadOnly

from .models import Category
from .serializers import CategoryListSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD API for product categories.
    Public: list and retrieve active categories.
    Staff: full create, update, delete.
    """

    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user and self.request.user.is_staff:
            return qs
        return qs.filter(is_active=True)
