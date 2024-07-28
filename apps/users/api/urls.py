from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import AdminLoginView

router = SimpleRouter()
app_name = 'users'
urlpatterns = [
    path('login/', AdminLoginView.as_view())
]
urlpatterns += router.urls
