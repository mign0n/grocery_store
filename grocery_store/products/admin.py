from django.contrib import admin

from products import models


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 3


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline, )
    list_display = (
        'name',
        'price',
        'sub_category',
        'slug',
    )


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'slug',
        'image',
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'image',
    )

