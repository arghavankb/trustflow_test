from .models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "amount", "description", "created_at", "created_by"]
        read_only_fields = ["id", "created_at", "created_by"]
