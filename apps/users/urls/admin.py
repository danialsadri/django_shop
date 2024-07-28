from django.urls import path
from rest_framework.routers import SimpleRouter
from apps.users.views.admin import AdminLoginView

router = SimpleRouter()
app_name = "users-admin"
urlpatterns = [
    path('login/', AdminLoginView.as_view())
]
urlpatterns += router.urls
