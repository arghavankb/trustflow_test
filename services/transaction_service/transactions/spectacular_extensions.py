from drf_spectacular.extensions import OpenApiAuthenticationExtension
from .authentication import JWTUserServiceAuthentication


class JWTBearerScheme(OpenApiAuthenticationExtension):
    target_class = 'transactions.authentication.JWTUserServiceAuthentication'  # full path
    name = 'BearerAuth'

    def get_security_definition(self, auto_schema):
        """
        Returns the OpenAPI security scheme for this authenticator.
        """
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }