from django.urls import path, include

app_name = 'api-v1'
urlpatterns = [
    path('users/', include('apps.users.api.v1.urls', namespace='users')),
    path('catalog/', include('apps.catalog.api.v1.urls', namespace='catalog')),
]
