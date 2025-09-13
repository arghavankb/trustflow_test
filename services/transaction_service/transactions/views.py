from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Transaction
from .serializers import TransactionSerializer
from .authentication import JWTUserServiceAuthentication


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [JWTUserServiceAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create Transaction",
        description="Create a new transaction.",
        tags=["Transactions"],
        request=TransactionSerializer,
        responses={201: TransactionSerializer},
        examples=[
            OpenApiExample(
                "Successful Transaction Creation",
                summary="Transaction is created",
                value={
                    "id": 1,
                    "amount": "200.00",
                    "description": "Payment for invoice #123",
                    "created_at": "2025-09-07T14:00:00Z",
                    "created_by": "arghavan",
                },
                response_only=True,
                status_codes=["201"],
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.username)



