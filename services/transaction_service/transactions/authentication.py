from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from types import SimpleNamespace
import jwt


class JWTUserServiceAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            username = payload.get("username", "anonymous")

            user = SimpleNamespace()
            user.username = username
            user.is_authenticated = True
            return user, token

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token is expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
