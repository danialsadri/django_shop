from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet

router = SimpleRouter()
router.register(prefix='category', viewset=CategoryViewSet, basename='category')
app_name = 'catalog'
urlpatterns = []
urlpatterns += router.urls
