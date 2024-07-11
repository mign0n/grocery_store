from django.urls import include, path

app_name = '%(app_label)s'


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
