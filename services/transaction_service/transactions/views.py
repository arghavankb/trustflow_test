from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Transaction
from .serializers import TransactionSerializer
from .authentication import JWTUserServiceAuthentication


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    authentication_classes = [JWTUserServiceAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

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
                    "created_by": "a.kb",
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

    @extend_schema(
        summary="List Transactions",
        description="Retrieve transactions. You can filter by `transaction_date` (required), `service_name`, "
                    "or `partner_name`.",
        tags=["Transactions"],
        parameters=[
            OpenApiParameter(
                name="transaction_date",
                description="Filter by transaction date (YYYY-MM-DD)",
                required=True,
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="partner_name",
                description="Filter by partner name",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="service_name",
                description="Filter by service name",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={200: TransactionSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Transaction.objects.none()

        transaction_date = self.request.query_params.get("transaction_date")
        if transaction_date is None:
            raise ValidationError({"transaction_date": "This query parameter is required."})

        queryset = Transaction.objects.filter(transaction_date=transaction_date)

        partner_name = self.request.query_params.get("partner_name")
        service_name = self.request.query_params.get("service_name")

        if service_name is not None:
            queryset = queryset.filter(service__name=service_name)
        if partner_name is not None:
            queryset = queryset.filter(partner__name=partner_name)

        return queryset
