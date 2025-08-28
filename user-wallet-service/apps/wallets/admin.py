from django.contrib import admin
from .models import Wallet, Holding
from apps.orders.models import Order

admin.site.register(Wallet)
admin.site.register(Holding)
admin.site.register(Order)


from django.contrib.auth.models import User
from apps.wallets.models import Wallet


