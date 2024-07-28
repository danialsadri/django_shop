from rest_framework.routers import SimpleRouter
from apps.catalog.views.admin import CategoryViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet)
urlpatterns = [] + router.urls
