from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.companies import Suppliers
from ..serializers import SupplierSerializer
from .. import utilities
from .. import firebaseauth
from ..models.stocktrackuser import Role
import datetime

class SupplierViewSet(viewsets.GenericViewSet):
   queryset = Suppliers.objects.all()
   serializer_class = SupplierSerializer
   
   def create(self, request):
        try:
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            # Ensure only admins/managers can create inventory items
            user_role = firebaseauth.get_user_role(firebase_token)
            if not Role.is_admin_or_manager(user_role):
                return utilities.FORBIDDEN
            
            supplier_data = {
                'supplier_id': request.data.get('supplier_id'),
                'supplier_name': request.data.get('supplier_name')
            }
            
            serializer = self.get_serializer(data=supplier_data)
            if not serializer.is_valid():
                return utilities.bad_request_response(serializer.errors)
            
            serializer.save()
            return utilities.created_response(serializer.data)
            
        except Exception as e:
            print(f"Error adding supplier: {str(e)}")
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
            
            suppliers = Suppliers.objects.all()
            if len(suppliers) == 0:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            
            serializer = self.get_serializer(suppliers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error listing suppliers: {str(e)}")
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
                supplier = Suppliers.objects.get(supplier_id=pk)
            except Suppliers.DoesNotExist:
                return utilities.NOT_FOUND
            
            serializer = self.get_serializer(supplier)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error retrieving supplier: {str(e)}")
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
                supplier = Suppliers.objects.get(supplier_id=pk)
            except Suppliers.DoesNotExist:
                return utilities.NOT_FOUND
            
            update_data = {
                'supplier_id': request.data.get('supplier_id', supplier.supplier_id),
                'supplier_name': request.data.get('supplier_name', supplier.supplier_name)
            }
            
            serializer = self.get_serializer(supplier, data=update_data)
            if not serializer.is_valid():
                print("Serializer errors:", serializer.errors)
                return utilities.bad_request_response(serializer.errors)
            
            serializer.save()
            return utilities.success_response(serializer.data)
            
        except Exception as e:
            print(f"Error updating supplier: {str(e)}")
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
                supplier = Suppliers.objects.get(supplier_id=pk)
            except Suppliers.DoesNotExist:
                return utilities.NOT_FOUND
            
            supplier.delete()
            return utilities.success_response("Successfully deleted supplier " + pk)
            
        except Exception as e:
            print(f"Error deleting supplier: {str(e)}")
            return utilities.SERVER_ERROR