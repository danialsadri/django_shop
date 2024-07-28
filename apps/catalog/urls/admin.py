from rest_framework.routers import SimpleRouter
from apps.catalog.views.admin import CategoryViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='Category')
app_name = 'catalog-admin'
urlpatterns = []
urlpatterns += router.urls
