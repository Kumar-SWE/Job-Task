from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order
from apps.wallets.models import Wallet, Holding
from decimal import Decimal, ROUND_DOWN
from django.db import transaction
from django.conf import settings
import requests

def fetch_current_price_inr(symbol_or_id: str):
    base = getattr(settings, "MARKET_DATA_BASE_URL", "http://127.0.0.1:8001").rstrip('/')
    sym = str(symbol_or_id).strip()


    cid = None
    try:
        r = requests.get(f"{base}/api/v1/currencies", timeout=5)
        if r.status_code == 200:
            for c in r.json():
                if c.get("id", "").lower() == sym.lower() or c.get("symbol", "").upper() == sym.upper():
                    cid = c.get("id")
                    break
    except Exception as e:
        print("Error resolving currency id:", e)
        return None

    if not cid:
        return None

  
    try:
        pr = requests.get(
            f"{base}/api/v1/prices",
            params={"ids": cid, "fiat": "inr"},
            timeout=5
        )
        if pr.status_code == 200:
            data = pr.json()
            mapping = data.get("__root__", data)
            entry = mapping.get(cid)
            if entry and "inr" in entry:
                return Decimal(str(entry["inr"]))
    except Exception as e:
        print("Error fetching price:", e)

    return None





@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders_view(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

   
    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    side = serializer.validated_data.get('side')
    symbol = serializer.validated_data.get('symbol').upper()
    qty = Decimal(serializer.validated_data.get('qty'))
    if qty <= 0:
        return Response({"detail":"Quantity must be > 0"}, status=status.HTTP_400_BAD_REQUEST)

   
    price = fetch_current_price_inr(symbol)
    if price is None:
        return Response({"detail":"Unable to fetch current price from market data service"},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)

    amount = (price * qty).quantize(Decimal('0.01'), rounding=ROUND_DOWN)


    with transaction.atomic():
        wallet, _ = Wallet.objects.select_for_update().get_or_create(
            user=request.user,
            defaults={'currency_code': 'INR', 'balance': 0}
        )

        if side == 'BUY':
            
            if wallet.balance < amount:
                Order.objects.create(
                    user=request.user, side=side, symbol=symbol, qty=qty,
                    price_inr=price, amount_inr=amount, status='REJECTED'
                )
                return Response({"detail": "Insufficient INR balance"}, status=status.HTTP_400_BAD_REQUEST)

          
            wallet.balance -= amount
            wallet.save()

        
            holding, created = Holding.objects.select_for_update().get_or_create(
                user=request.user, symbol=symbol,
                defaults={'quantity': 0, 'avg_cost_inr': 0}
            )
            prev_qty = holding.quantity
            prev_cost = holding.avg_cost_inr
            new_total_qty = (prev_qty + qty)
            if new_total_qty > 0:
                new_avg = ((prev_qty * prev_cost) + amount) / new_total_qty
            else:
                new_avg = amount / qty

            holding.quantity = new_total_qty
            holding.avg_cost_inr = new_avg
            holding.save()

            order = Order.objects.create(
                user=request.user, side=side, symbol=symbol, qty=qty,
                price_inr=price, amount_inr=amount, status='COMPLETED'
            )
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        elif side == 'SELL':
          
            try:
                holding = Holding.objects.select_for_update().get(user=request.user, symbol=symbol)
            except Holding.DoesNotExist:
                Order.objects.create(
                    user=request.user, side=side, symbol=symbol, qty=qty,
                    price_inr=price, amount_inr=amount, status='REJECTED'
                )
                return Response({"detail": "No holdings for this symbol"}, status=status.HTTP_400_BAD_REQUEST)

            if holding.quantity < qty:
                Order.objects.create(
                    user=request.user, side=side, symbol=symbol, qty=qty,
                    price_inr=price, amount_inr=amount, status='REJECTED'
                )
                return Response({"detail": "Insufficient holdings quantity"}, status=status.HTTP_400_BAD_REQUEST)

           
            holding.quantity -= qty
            if holding.quantity == 0:
                holding.avg_cost_inr = 0
            holding.save()

           
            wallet.balance += amount
            wallet.save()

            order = Order.objects.create(
                user=request.user, side=side, symbol=symbol, qty=qty,
                price_inr=price, amount_inr=amount, status='COMPLETED'
            )
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        else:
            return Response({"detail": "Invalid side, must be BUY or SELL"}, status=status.HTTP_400_BAD_REQUEST)






