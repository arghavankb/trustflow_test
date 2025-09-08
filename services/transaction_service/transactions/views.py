from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import TransactionSerializer
from .authentication import JWTUserServiceAuthentication


class TransactionViewSet(viewsets.ViewSet):
    authentication_classes = [JWTUserServiceAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=TransactionSerializer,
        responses={201: TransactionSerializer},
        examples=[
            OpenApiExample(
                "Successful Transaction Creation",
                summary="Transaction created",
                value={
                    "id": 1,
                    "amount": "200.00",
                    "description": "Payment for invoice #123",
                    "created_at": "2025-09-07T14:00:00Z",
                    "created_by": "arghavan",
                },
                response_only=True,
                status_codes=["201"],
            ),
        ],
        summary="Create Transaction",
        description="Create a new transaction.",
        tags=["Transactions"],
    )
    def create(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

