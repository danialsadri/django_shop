from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, CategoryFrontViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='Category')
router.register('categories-front', CategoryFrontViewSet)
app_name = 'catalog'
urlpatterns = []
urlpatterns += router.urls
