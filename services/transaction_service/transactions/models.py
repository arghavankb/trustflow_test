from django.db import models


class Transaction(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=150)

    def __str__(self):
        return f"Transaction {self.id} by user {self.created_by}"

