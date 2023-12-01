from django.db import models
from users.models import User
from datetime import datetime

SERVICES_CHOICES = [
    ('Transferencias Internas', 'Transferencias Internas'),
    ('Transferencias Otros Bancos', 'Transferencias Otros Bancos'),
]

class FinancialEntity(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    service = models.CharField(max_length=255, choices=SERVICES_CHOICES)
    date_time_transaction = models.DateTimeField()
    title = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=255, blank=True, null=True)

    origin_name = models.CharField(max_length=255, blank=True, null=True)
    origin_account = models.CharField(max_length=255, blank=True, null=True)
    origin_financial_entity = models.ForeignKey(FinancialEntity, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_origin')

    destination_name = models.CharField(max_length=255)
    destination_account = models.CharField(max_length=255)
    destination_financial_entity = models.ForeignKey(FinancialEntity, on_delete=models.CASCADE, related_name='transactions_destination')

    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='registered_by')
    date_time_registered = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"Transaction - {self.service} - {self.date_time_transaction}"

