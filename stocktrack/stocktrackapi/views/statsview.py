import datetime
from rest_framework import viewsets
from ..models.orders import PurchaseOrder
from ..models.stocktrackuser import StockTrackUser
from ..models.inventory import Part
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework import status
from ..serializers import StatsSerializer


# /stats/10-12-2024
# {
#     'revenue': 50000,
#     'num_customers': 50,
#     'num_orders': 500,
#     'num_low_stock_items': 5
# }

class StatsViewSet(viewsets.GenericViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = StatsSerializer

    def retrieve(self, request, pk=None):
        try:
            date = datetime.strptime(pk, '%d-%m-%Y').date()
            
            revenue = 0

            for i in PurchaseOrder.objects.filter(created=date, is_outbound=True):
                revenue += i.value
                
            num_customers = StockTrackUser.objects.filter(
                role='customer'
            ).count()
            
            num_orders = PurchaseOrder.objects.filter(
                created=date
            ).count()
            
            num_low_stock_items = 0
            for i in Part.objects.all():
                if i.stock_level < i.reorder_point:
                    num_low_stock_items += 1
            
            return Response({
                'revenue': revenue,
                'num_customers': num_customers,
                'num_orders': num_orders,
                'num_low_stock_items': num_low_stock_items
            })
            
        except ValueError:
            return Response({'error': 'Invalid date format. Use DD-MM-YYYY'},status=status.HTTP_400_BAD_REQUEST)
