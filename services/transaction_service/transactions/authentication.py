import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTUserServiceAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Authorization header is missing")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            request.username_from_token = payload.get('username', 'anonymous')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token is expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")


