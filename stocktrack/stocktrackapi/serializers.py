from rest_framework import serializers

from models.stocktrackuser import StockTrackUser
from models.orders import PurchaseOrder

# We can choose to do classes or just put them all in here,
# probably classes to keep it neater

class StockTrackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTrackUser
        fields = ('__all__')

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('__all__')
        
class Stock