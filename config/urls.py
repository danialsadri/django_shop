from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/swagger/file/', SpectacularAPIView.as_view(), name='schema'),
    path('api/users/', include('apps.users.api.urls', namespace='users')),
    path('api/catalog/', include('apps.catalog.api.urls', namespace='catalog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = "django_shop"
admin.site.index_title = "django_shop"
admin.site.site_header = "django_shop"
