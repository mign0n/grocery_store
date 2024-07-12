from api import views
from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = '%(app_label)s'

router = SimpleRouter()
router.register('categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
