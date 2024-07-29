from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='Category')
app_name = 'catalog'
urlpatterns = []
urlpatterns += router.urls
