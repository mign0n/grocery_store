from decimal import Decimal
from typing import OrderedDict

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
    item_cost = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'id',
            'owner',
            'product',
            'amount',
            'item_cost',
        )
        read_only_fields = ('id',)

    def get_item_cost(self, obj: Cart) -> Decimal:
        return obj.product.price * obj.amount

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
