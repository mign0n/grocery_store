from decimal import Decimal
from typing import OrderedDict

from django.db import models
from rest_framework import serializers

from products.models import Cart, Category, Product, ProductImage, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = (
            'id',
            'name',
            'slug',
            'image',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'image',
        )


class CategoryWithSubSerializer(CategorySerializer):
    sub_category = SubCategorySerializer(source='subcategory', many=True)

    class Meta:
        model = SubCategory
        fields = (
            *CategorySerializer.Meta.fields,
            'sub_category',
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'id',
            'image',
        )


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='sub_category.category')
    sub_category = SubCategorySerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'category',
            'sub_category',
            'price',
            'images',
        )


class CartSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = (
            'id',
            'owner',
            'product',
            'amount',
        )
        read_only_fields = ('id',)

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        product = attrs.get('product')
        if not product:
            raise serializers.ValidationError('The product field is required.')
        if not Product.objects.filter(pk=product.pk).exists():
            raise serializers.ValidationError('The object is not exists.')
        if self.Meta.model.objects.filter(
            owner=attrs.get('owner'),
            product=product,
        ).exists():
            raise serializers.ValidationError(
                'The fields owner, product must make a unique set.',
            )
        return attrs


class CartListSerializer(serializers.Serializer):
    count = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'count',
            'total_price',
            'items',
        )

    def get_count(self, obj: models.Model) -> int:
        return self.context['count']

    def get_total_price(self, obj: models.Model) -> Decimal:
        return self.context['total_price']

    @staticmethod
    def get_items(obj: models.Model) -> list[models.Model]:
        return [item for item in obj]
