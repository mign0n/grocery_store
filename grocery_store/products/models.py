from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AbstractBaseModel(models.Model):
    name = models.CharField(
        verbose_name='наименование',
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='слаг-имя',
        max_length=200,
        unique=True,
    )

    class Meta:
        abstract = True
        default_related_name = '%(class)s'

    def __repr__(self) -> str:
        return '{}: pk={}, name={}, slug={}'.format(
            type(self).__name__,
            self.pk,
            self.name,
            self.slug,
        )

    def __str__(self) -> str:
        return self.name


class Category(AbstractBaseModel):
    """Модель категорий продуктов."""

    image = models.ImageField(
        verbose_name='изображение',
        upload_to=settings.CATEGORY_IMAGE_PATH,
        blank=True,
    )


class SubCategory(AbstractBaseModel):
    """Модель подкатегорий продуктов."""

    image = models.ImageField(
        verbose_name='изображение',
        upload_to=settings.SUBCATEGORY_IMAGE_PATH,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='категория продукта',
        null=True,
    )


class Product(AbstractBaseModel):
    """Модель продуктов."""

    image = models.ImageField(
        verbose_name='изображение',
        upload_to=settings.PRODUCT_IMAGE_PATH,
        blank=True,
    )
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=6,
        decimal_places=2,
    )
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        verbose_name='подкатегория продукта',
        null=True,
    )


class Cart(models.Model):
    """Модель корзины."""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='владелец корзины',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='продукт',
    )

    class Meta:
        default_related_name = '%(class)s'
        constraints = [
            models.UniqueConstraint(
                fields=('owner', 'product'),
                name='unique_%(class)s_product',
            ),
        ]

    def __repr__(self) -> str:
        return '{}: pk={}, owner={}, product={}'.format(
            type(self).__name__,
            self.pk,
            self.owner.name,
            self.product.name,
        )
