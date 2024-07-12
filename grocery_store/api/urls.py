from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api import views

app_name = '%(app_label)s'

router = SimpleRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('products', views.ProductsViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
