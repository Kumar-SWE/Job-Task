from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','user','side','symbol','qty','price_inr','amount_inr','status','created_at')
        read_only_fields = ('user','price_inr','amount_inr','status','created_at')
