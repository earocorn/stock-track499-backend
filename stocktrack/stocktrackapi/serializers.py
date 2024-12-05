from rest_framework import serializers

from .models.stocktrackuser import StockTrackUser
from .models.orders import PurchaseOrder
from .models.inventory import Part
from .models.companies import Suppliers
from .models.companies import Manufacturers

class StockTrackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTrackUser
        fields = ('__all__')

class PurchaseOrderSerializer(serializers.ModelSerializer):

    due_date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d", "%m/%d/%Y"])

    class Meta:
        model = PurchaseOrder
        fields = ('__all__')
        
class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ('__all__')

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ('__all__')

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturers
        fields = ('__all__')

