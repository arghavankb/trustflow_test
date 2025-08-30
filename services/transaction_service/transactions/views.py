import jwt
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .authentication import JWTUserServiceAuthentication
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-id')
    serializer_class = TransactionSerializer
    authentication_classes = [JWTUserServiceAuthentication]
    permission_classes = []

    def perform_create(self, serializer):
        username = getattr(self.request, 'username_from_token', 'anonymous')
        serializer.save(created_by=username)
