from django.urls import path
from rest_framework.routers import SimpleRouter
from apps.users.views.admin import AdminLoginView

router = SimpleRouter()
urlpatterns = [
    path('login/', AdminLoginView.as_view())
]
urlpatterns += router.urls
