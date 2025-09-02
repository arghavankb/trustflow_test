from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "department",
            "title",
        )


class LDAPLoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class LoginErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class RefreshTokenRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
