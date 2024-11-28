from rest_framework import viewsets
from ..models.orders import PurchaseOrder
from ..serializers import PurchaseOrderSerializer

class InventoryViewSet(viewsets.GenericViewSet):
   queryset = PurchaseOrder.objects.all()
   serializer_class = PurchaseOrderSerializer
   
   def create(self, request):
       pass
   
   def list(self, request):
       pass
   
   def retrieve(self, request, pk=None):
       pass
   
   def update(self, request, pk=None):
       pass
   
   def destroy(self, request, pk=None):
       pass