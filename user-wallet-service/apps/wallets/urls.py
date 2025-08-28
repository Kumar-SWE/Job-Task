from django.urls import path
from .views import wallet_view, holdings_view

urlpatterns = [
    path('wallet', wallet_view, name='wallet'),
    path('holdings', holdings_view, name='holdings'),
]
