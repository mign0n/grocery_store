from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter

from api import views

app_name = '%(app_label)s'

router = SimpleRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('products', views.ProductsViewSet, basename='product')
router.register('cart', views.CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(url_name='api:schema'),
        name='docs',
    ),
]
