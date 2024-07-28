from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

admin_urls = [
    path('api/admin/users/', include('apps.users.urls.admin', namespace='users-admin')),
    path('api/admin/catalog/', include('apps.catalog.urls.admin', namespace='catalog-admin'))
]

front_urls = [
    path('api/front/users/', include('apps.users.urls.front', namespace='users-front')),
    path('api/front/catalog/', include('apps.catalog.urls.front', namespace='catalog-front'))
]

doc_patterns = [
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/swagger/file/', SpectacularAPIView.as_view(), name='schema'),
]

urlpatterns = [
    path("admin/", admin.site.urls),
]
urlpatterns += front_urls + admin_urls + doc_patterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = "django_shop"
admin.site.index_title = "django_shop"
admin.site.site_header = "django_shop"
