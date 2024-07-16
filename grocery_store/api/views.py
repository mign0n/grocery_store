from django.db.models import F, QuerySet, Sum
from rest_framework import mixins, status, viewsets
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


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = None
    serializer_class = serializers.CartSerializer

    def get_queryset(self) -> QuerySet:
        return Cart.objects.filter(owner=self.request.user)

    @action(methods=('DELETE',), detail=False)  # type: ignore
    def empty(self, request: Request) -> Response:
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=('GET',), detail=False)  # type: ignore
    def show(self, request: Request) -> Response:
        cart_items = (
            self.get_queryset()
            .values(
                'id',
                'product_id',
                'product__name',
                'product__price',
                'amount',
            )
            .order_by('product__name')
        )
        return Response(
            serializers.CartListSerializer(
                cart_items,
                context={
                    'count': cart_items.count(),
                    'total_price': cart_items.aggregate(
                        total_price=Sum(F('product__price') * F('amount')),
                    ).get('total_price'),
                },
            ).data,
        )
