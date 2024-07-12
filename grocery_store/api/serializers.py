from rest_framework import serializers

from products.models import Category, Product, ProductImage, SubCategory


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

    class Meta(CategorySerializer.Meta):
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
