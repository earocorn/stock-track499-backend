from rest_framework import serializers

from .models.stocktrackuser import StockTrackUser
from .models.orders import PurchaseOrder
from .models.inventory import Part

class StockTrackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTrackUser
        fields = ('__all__')

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('__all__')
        
class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ('__all__')