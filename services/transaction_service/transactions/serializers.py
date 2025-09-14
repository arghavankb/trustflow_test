from .models import Transaction, Service, Partner
from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name"]


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ["id", "name"]


class TransactionSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source="service", write_only=True
    )

    partner = PartnerSerializer(read_only=True)
    partner_id = serializers.PrimaryKeyRelatedField(
        queryset=Partner.objects.all(), source="partner", write_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "description",
            "created_at",
            "created_by",
            "transaction_date",
            "partner",
            "partner_id",
            "service",
            "service_id"
        ]
        read_only_fields = ["id", "created_at", "created_by"]
