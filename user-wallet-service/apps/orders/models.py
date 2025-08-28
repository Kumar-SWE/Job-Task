from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Order(models.Model):
    SIDE_CHOICES = (('BUY','BUY'), ('SELL','SELL'))
    STATUS_CHOICES = (('PENDING','PENDING'), ('COMPLETED','COMPLETED'), ('REJECTED','REJECTED'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    side = models.CharField(max_length=4, choices=SIDE_CHOICES)
    symbol = models.CharField(max_length=20)
    qty = models.DecimalField(max_digits=30, decimal_places=8)
    price_inr = models.DecimalField(max_digits=20, decimal_places=2)
    amount_inr = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} {self.side} {self.symbol} {self.qty}"
