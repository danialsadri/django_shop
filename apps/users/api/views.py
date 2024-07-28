from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import AdminLoginSerializer


class AdminLoginView(ObtainAuthToken):
    serializer_class = AdminLoginSerializer
