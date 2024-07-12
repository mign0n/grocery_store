from rest_framework import serializers

from products.models import AbstractBaseModel, Category, SubCategory


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
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'image',
            'sub_category',
        )

    @staticmethod
    def get_sub_category(obj: AbstractBaseModel) -> list[dict]:
        return SubCategorySerializer(obj.subcategory.all(), many=True).data
