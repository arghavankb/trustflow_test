from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample

from .backends import LDAPBackend
from .models import CustomUser
from .serializers import (
    UserSerializer,
    LDAPLoginRequestSerializer,
    LoginResponseSerializer,
    LoginErrorResponseSerializer,
)


class LoginAPIView(APIView):

    @extend_schema(
        request=LDAPLoginRequestSerializer,
        responses={
            200: LoginResponseSerializer,
            401: LoginErrorResponseSerializer,
            503: LoginErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                "Successful login",
                summary="JWT login example",
                value={
                    "user": {
                        "id": 1,
                        "email": "a.kazembakhshi@toman.ir",
                        "username": "a.kazembakhshi",
                        "first_name": "Arghavan",
                        "last_name": "Kb",
                        "department": "Tech-Data",
                        "title": "Backend Developer",
                    },
                    "access_token": "eyJhbGciOiJIUzI1...",
                    "refresh_token": "eyJhbGciOiJIUzI1...",
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Invalid credentials",
                summary="Login failed example",
                value={"detail": "Invalid email or password"},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                "LDAP service error",
                summary="LDAP authentication service error",
                value={"detail": "LDAP authentication service error: <error_message>"},
                response_only=True,
                status_codes=["503"],
            ),
        ],
        description="Authenticate user with LDAP and return JWT tokens",
        summary="Login with LDAP",
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = LDAPLoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            ldap_data = LDAPBackend().authenticate(request, email, password)
        except Exception as e:
            return Response(
                {"detail": f"LDAP authentication service error: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if not ldap_data:
            return Response(
                {"detail": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user, _ = CustomUser.objects.get_or_create(email=email)
        user.username = ldap_data["username"]
        user.first_name = ldap_data["first_name"]
        user.last_name = ldap_data["last_name"]
        user.department = ldap_data["department"]
        user.title = ldap_data["title"]
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        refresh["username"] = user.username
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        user_data = UserSerializer(user).data

        return Response(
            {
                "user": user_data,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK,
        )
