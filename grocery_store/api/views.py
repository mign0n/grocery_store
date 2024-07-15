from django.db.models import QuerySet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api import serializers
from api.permissions import ReadOnly
from products.models import Cart, Category, Product


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (ReadOnly,)
    queryset = Category.objects.all().order_by('id')
    serializer_class = serializers.CategoryWithSubSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    permission_classes = (ReadOnly,)
    queryset = Product.objects.all().order_by('id')
    serializer_class = serializers.ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    pagination_class = None
    serializer_class = serializers.CartSerializer

    def get_queryset(self) -> QuerySet:
        return Cart.objects.filter(owner=self.request.user).all()

    @action(methods=('DELETE',), detail=False)  # type: ignore
    def empty(self, request: Request) -> Response:
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
