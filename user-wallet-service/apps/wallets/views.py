from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.wallets.serializers import WalletSerializer, HoldingSerializer
from apps.wallets.models import Wallet, Holding
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wallet_view(request):
    wallet, _ = Wallet.objects.get_or_create(user=request.user, defaults={'currency_code':'INR', 'balance':0})
    serializer = WalletSerializer(wallet)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def holdings_view(request):
    holdings = Holding.objects.filter(user=request.user)
    serializer = HoldingSerializer(holdings, many=True)
    return Response(serializer.data)
