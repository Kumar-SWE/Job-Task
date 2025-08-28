from rest_framework import serializers
from .models import Wallet, Holding

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('currency_code', 'balance', 'locked', 'updated_at')

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ('id', 'symbol', 'quantity', 'avg_cost_inr', 'updated_at')
