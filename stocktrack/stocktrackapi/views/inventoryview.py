from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.inventory import Part
from ..serializers import PartSerializer
from .. import utilities
from .. import firebaseauth
from ..models.stocktrackuser import Role
import datetime

class InventoryViewSet(viewsets.GenericViewSet):
   queryset = Part.objects.all()
   serializer_class = PartSerializer
   
   def create(self, request):
        try:
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            # Ensure only admins/managers can create inventory items
            user_role = firebaseauth.get_user_role(firebase_token)
            if not Role.is_admin_or_manager(user_role):
                return utilities.FORBIDDEN
            
            part_data = {
                'part_name': request.data.get('part_name'),
                'part_number': request.data.get('part_number'),
                'supplier_id': request.data.get('supplier_id'),
                'inbound_price': request.data.get('inbound_price'),
                'outbound_price': request.data.get('outbound_price'),
                'lead_time': request.data.get('lead_time', 2),
                'stock_level': request.data.get('stock_level', 0),
                'reorder_point': request.data.get('reorder_point')
            }
            
            serializer = self.get_serializer(data=part_data)
            if not serializer.is_valid():
                return utilities.bad_request_response(serializer.errors)
            
            serializer.save()
            return utilities.created_response(serializer.data)
            
        except Exception as e:
            print(f"Error adding part: {str(e)}")
            return utilities.SERVER_ERROR

   def list(self, request):
        try:
            if not request.META.get('HTTP_AUTHORIZATION'):
                return utilities.UNAUTHORIZED
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            user_role = firebaseauth.get_user_role(firebase_token)
            
            # Only allow admin, manager, and employee to view inventory
            if not (Role.is_admin_or_manager(user_role) or Role.is_employee(user_role)):
                return utilities.FORBIDDEN
            
            print(self.queryset)
            print(len(self.queryset))
            parts = self.queryset
            if len(parts) == 0:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            
            serializer = self.get_serializer(parts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error listing parts: {str(e)}")
            return utilities.SERVER_ERROR
   
   def retrieve(self, request, pk=None):
        try:
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            user_role = firebaseauth.get_user_role(firebase_token)
            
            # Only allow admin, manager, and employee to retrieve inventory
            if not (Role.is_admin_or_manager(user_role) or user_role == Role.EMPLOYEE):
                return utilities.FORBIDDEN
            
            try:
                part = Part.objects.get(part_number=pk)
            except Part.DoesNotExist:
                return utilities.NOT_FOUND
            
            serializer = self.get_serializer(part)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error retrieving part: {str(e)}")
            return utilities.SERVER_ERROR
   
   def update(self, request, pk=None):
        try:
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            user_role = firebaseauth.get_user_role(firebase_token)
            if not Role.is_admin_or_manager(user_role):
                return utilities.FORBIDDEN
            
            try:
                part = Part.objects.get(part_number=pk)
            except Part.DoesNotExist:
                return utilities.NOT_FOUND
            
            update_data = {
                'part_name': request.data.get('part_name', part.part_name),
                'part_number': request.data.get('part_number', part.part_number),
                'supplier_id': request.data.get('supplier_id', part.supplier_id),
                'inbound_price': request.data.get('inbound_price', part.inbound_price),
                'outbound_price': request.data.get('outbound_price', part.outbound_price),
                'stock_level': request.data.get('stock_level', part.stock_level),
                'reorder_point': request.data.get('reorder_point', part.reorder_point),
                'lead_time': request.data.get('lead_time', part.lead_time)
            }
            
            serializer = self.get_serializer(part, data=update_data)
            if not serializer.is_valid():
                print("Serializer errors:", serializer.errors)
                return utilities.bad_request_response(serializer.errors)
            
            serializer.save()
            return utilities.success_response(serializer.data)
            
        except Exception as e:
            print(f"Error updating part: {str(e)}")
            return utilities.SERVER_ERROR
   
   def destroy(self, request, pk=None):
        try:
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            user_role = firebaseauth.get_user_role(firebase_token)
            if not Role.is_admin_or_manager(user_role):
                return utilities.FORBIDDEN
            
            try:
                part = Part.objects.get(part_number=pk)
            except Part.DoesNotExist:
                return utilities.NOT_FOUND
            
            part.delete()
            return utilities.success_response("Successfully deleted part " + pk)
            
        except Exception as e:
            print(f"Error deleting part: {str(e)}")
            return utilities.SERVER_ERROR