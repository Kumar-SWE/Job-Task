from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    currency_code = models.CharField(max_length=10, default='INR')
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    locked = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.currency_code} : {self.balance}"

class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='holdings')
    symbol = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=30, decimal_places=8, default=Decimal('0'))
    avg_cost_inr = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'symbol')

    def __str__(self):
        return f"{self.user.email} - {self.symbol} : {self.quantity}"
