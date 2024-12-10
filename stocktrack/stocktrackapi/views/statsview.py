from datetime import datetime
from rest_framework import viewsets
from ..models.orders import PurchaseOrder
from ..models.stocktrackuser import StockTrackUser
from ..models.inventory import Part
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework import status
from rest_framework import serializers


# /stats/10-12-2024
# {
#     'revenue': 50000,
#     'num_customers': 50,
#     'num_orders': 500,
#     'num_low_stock_items': 5
# }

class Stats(object):
    def __init__(self, **kwargs):
        for field in ('revenue', 'num_customers', 'num_orders', 'num_low_stock_items'):
            setattr(self, field, kwargs.get(field, None))
            
            
class StatsSerializer(serializers.Serializer):
    revenue = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    num_customers = serializers.IntegerField(read_only=True)
    num_orders = serializers.IntegerField(read_only=True)
    num_low_stock_items = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return Stats(id=None, **validated_data)


class StatsViewSet(viewsets.GenericViewSet):

    def retrieve(self, request, pk=None):
        try:
            date = datetime.strptime(pk, '%m-%d-%Y').date()
            
            revenue = 0

            for i in PurchaseOrder.objects.filter(created=date, is_outbound=True):
                revenue += i.value
                
            num_customers = StockTrackUser.objects.filter(
                role='customer'
            ).count()
            
            num_orders = PurchaseOrder.objects.filter(
                created=date
            ).count()


            num_low_stock_items = Part.objects.filter(
                status='Low Stock'
            ).count()
            
            stats = {
                'revenue': revenue,
                'num_customers': num_customers,
                'num_orders': num_orders,
                'num_low_stock_items': num_low_stock_items
            }
            
            return Response(stats)
            
        except ValueError:
            return Response({'error': 'Invalid date format. Use DD-MM-YYYY'},status=status.HTTP_400_BAD_REQUEST)
