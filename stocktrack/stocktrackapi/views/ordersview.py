from rest_framework import viewsets
from django.db import transaction
from datetime import datetime
from ..models.orders import PurchaseOrder
from ..models.inventory import Part
from ..models.stocktrackuser import Role
from ..serializers import PurchaseOrderSerializer
from .. import utilities
from .. import firebaseauth

class OrdersViewSet(viewsets.GenericViewSet):
    queryset = PurchaseOrder.objects.all().order_by('created')
    serializer_class = PurchaseOrderSerializer
    
    @transaction.atomic
    def create(self, request):
        try:
            try:
                firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            except:
                return utilities.UNAUTHORIZED
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            user_role = firebaseauth.get_user_role(firebase_token)
            decoded_token = firebaseauth.get_decoded_token(firebase_token)
            
            is_outbound = request.data.get('is_outbound', True)
            
            if user_role == Role.CUSTOMER and not is_outbound:
                return utilities.FORBIDDEN
            
            if not is_outbound and not Role.is_admin_or_manager(user_role):
                return utilities.FORBIDDEN
                
            try:
                part = Part.objects.get(part_number=request.data.get('part_number'))
                qty = int(request.data.get('qty', 0))
                
                if is_outbound:
                    if part.stock_level < qty:
                        return utilities.bad_request_response("Insufficient stock level")
                    
                    value = part.outbound_price * qty
                else:
                    value = part.inbound_price * qty
                
            except Part.DoesNotExist:
                return utilities.bad_request_response("Part not found")
            
            order_data = {
#                 'po_number': request.data.get('po_number'),
                'part_name': request.data.get('part_name'),
                'part_number': request.data.get('part_number'),
                'supplier_id': request.data.get('supplier_id'),
                'qty': qty,
                'due_date': datetime.strptime(request.data['due_date'], "%Y-%m-%d").date(),
                'created': datetime.now().date(),
                'value': value,
                'customer_id': decoded_token.get('uid'),
                'is_outbound': is_outbound,
                'status': request.data.get('status'),
            }
            
            serializer = self.get_serializer(data=order_data)
            if not serializer.is_valid():
                return utilities.bad_request_response(serializer.errors)
            
            serializer.save()
            
            return utilities.created_response(serializer.data)
            
        except Exception as e:
            print(f"Error creating order: {str(e)}")
            return utilities.SERVER_ERROR
    
    def list(self, request):
        try:
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            user_role = firebaseauth.get_user_role(firebase_token)
            decoded_token = firebaseauth.get_decoded_token(firebase_token)
            
            orders = self.queryset
            if user_role == Role.CUSTOMER:
                orders = orders.filter(
                    customer_id=decoded_token.get('uid'),
                    is_outbound=True
                )
            
            serializer = self.get_serializer(orders, many=True)
            return utilities.success_response(serializer.data)
            
        except Exception as e:
            print(f"Error listing orders: {str(e)}")
            return utilities.SERVER_ERROR
    
    def retrieve(self, request, pk=None):
        try:
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            user_role = firebaseauth.get_user_role(firebase_token)
            decoded_token = firebaseauth.get_decoded_token(firebase_token)
            
            try:
                order = PurchaseOrder.objects.get(pk=pk)
                
                if user_role == Role.CUSTOMER:
                    if not (order.customer_id == decoded_token.get('uid') and order.is_outbound):
                        return utilities.FORBIDDEN
                
                serializer = self.get_serializer(order)
                return utilities.success_response(serializer.data)
                
            except PurchaseOrder.DoesNotExist:
                return utilities.NOT_FOUND
                
        except Exception as e:
            print(f"Error retrieving order: {str(e)}")
            return utilities.SERVER_ERROR
    
    @transaction.atomic
    def update(self, request, pk=None):
        try:
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            user_role = firebaseauth.get_user_role(firebase_token)
            if not Role.is_admin_or_manager(user_role):
                return utilities.FORBIDDEN
            
            try:
                order = PurchaseOrder.objects.get(pk=pk)
                part = Part.objects.get(part_number=order.part_number)
                
                if order.is_outbound:
                    if PurchaseOrder.status == "Shipped":
                        part.stock_level -= order.qty
                else:
                    if PurchaseOrder.status == "Received":
                        part.stock_level += order.qty
                
                part.save()
                
                serializer = self.get_serializer(order, data=request.data, partial=True)
                if not serializer.is_valid():
                    return utilities.bad_request_response(serializer.errors)
                
                serializer.save()
                return utilities.success_response_with_data(serializer.data)
                
            except PurchaseOrder.DoesNotExist:
                return utilities.NOT_FOUND
                
        except Exception as e:
            print(f"Error updating order: {str(e)}")
            return utilities.SERVER_ERROR
    
    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            # Only admin/manager can delete orders
            user_role = firebaseauth.get_user_role(firebase_token)
            if not Role.is_admin_or_manager(user_role):
                return utilities.FORBIDDEN
            
            try:
                order = PurchaseOrder.objects.get(pk=pk)
                part = Part.objects.get(part_number=order.part_number)
                
                if order.is_outbound:
                    part.stock_level += order.qty
                else:
                    part.stock_level -= order.qty
                
                part.save()
                order.delete()
                
                return utilities.success_response("Successfully deleted order " + pk)
                
            except PurchaseOrder.DoesNotExist:
                return utilities.NOT_FOUND
                
        except Exception as e:
            print(f"Error deleting order: {str(e)}")
            return utilities.SERVER_ERROR