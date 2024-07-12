from rest_framework import viewsets

from api import serializers
from api.permissions import ReadOnly
from products.models import Category, Product


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (ReadOnly,)
    queryset = Category.objects.all().order_by('id')
    serializer_class = serializers.CategoryWithSubSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    permission_classes = (ReadOnly,)
    queryset = Product.objects.all().order_by('id')
    serializer_class = serializers.ProductSerializer
