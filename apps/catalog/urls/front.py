from rest_framework.routers import SimpleRouter
from apps.catalog.views.front import CategoryViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet)
app_name = 'catalog-front'
urlpatterns = []
urlpatterns += router.urls
