from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.companies import Manufacturers
from ..serializers import ManufacturerSerializer
from .. import utilities
from .. import firebaseauth
from ..models.stocktrackuser import Role
import datetime

class ManufacturerViewSet(viewsets.GenericViewSet):
   queryset = Manufacturers.objects.all()
   serializer_class = ManufacturerSerializer
   
   def create(self, request):
        try:
            firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            if not firebase_token:
                return utilities.UNAUTHORIZED
            
            # Ensure only admins/managers can create inventory items
            user_role = firebaseauth.get_user_role(firebase_token)
            if not Role.is_admin_or_manager(user_role):
                return utilities.FORBIDDEN
            
            manufacturer_data = {
                'manufacturer_ID': request.data.get('manufacturer_ID'),
                'manufacturer_name': request.data.get('manufacturer_name')
            }
            
            serializer = self.get_serializer(data=manufacturer_data)
            if not serializer.is_valid():
                return utilities.bad_request_response(serializer.errors)
            
            serializer.save()
            return utilities.created_response(serializer.data)
            
        except Exception as e:
            print(f"Error adding manufacturer: {str(e)}")
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
            manufacturers = self.queryset
            if len(manufacturers) == 0:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            
            serializer = self.get_serializer(manufacturers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error listing manufacturers: {str(e)}")
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
                manufacturer = Manufacturers.objects.get(manufacturer_ID=pk)
            except Manufacturers.DoesNotExist:
                return utilities.NOT_FOUND
            
            serializer = self.get_serializer(manufacturer)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error retrieving manufacturer: {str(e)}")
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
                manufacturer = Manufacturers.objects.get(manufacturer_ID=pk)
            except Manufacturers.DoesNotExist:
                return utilities.NOT_FOUND
            
            update_data = {
                'manufacturer_ID': request.data.get('manufacturer_ID', manufacturer.manufacturer_ID),
                'manufacturer_name': request.data.get('manufacturer_name', manufacturer.manufacturer_name)
            }
            
            serializer = self.get_serializer(manufacturer, data=update_data)
            if not serializer.is_valid():
                print("Serializer errors:", serializer.errors)
                return utilities.bad_request_response(serializer.errors)
            
            serializer.save()
            return utilities.success_response(serializer.data)
            
        except Exception as e:
            print(f"Error updating manufacturer: {str(e)}")
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
                manufacturer = Manufacturers.objects.get(manufacturer_ID=pk)
            except Manufacturers.DoesNotExist:
                return utilities.NOT_FOUND
            
            manufacturer.delete()
            return utilities.success_response("Successfully deleted manufacturer " + pk)
            
        except Exception as e:
            print(f"Error deleting manufacturer: {str(e)}")
            return utilities.SERVER_ERROR