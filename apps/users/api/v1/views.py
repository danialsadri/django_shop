from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import LoginSerializer


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
