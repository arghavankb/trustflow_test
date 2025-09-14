from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=150)
    transaction_date = models.DateField()
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT, related_name="transactions")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="transactions")

    def __str__(self):
        return f"Transaction {self.id} by user {self.created_by}"

