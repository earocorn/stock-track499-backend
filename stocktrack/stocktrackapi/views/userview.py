import datetime
import secrets
from rest_framework import viewsets
from rest_framework.decorators import action, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import viewsets
from stocktrackapi.models.stocktrackuser import StockTrackUser
from stocktrackapi.serializers.serializers import StockTrackUserSerializer
import firebaseauth

from firebase_admin import auth

unauthorizedResponse = Response({'error': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
invalidResponse = Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

# Add user
# Add inventory
# Add order

class StockTrackUserViewset(viewsets.GenericViewSet):
    queryset = StockTrackUser.objects.all().order_by('created')
    serializer_class = StockTrackUserSerializer

    #   actions authenticated by firebase_id_token and is_admin method 
    #   to check if user has permission is_staff

    def list(self, request):
        firebase_id_token = request.query_params.get('firebase_id_token')
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        if(False):
            return unauthorizedResponse
        
    #accepts arguments email and username to create a default firebase/database user
    @action(detail=False, methods=['post'], url_path='create_dual_user')
    def create_dual_user(self, request):
        firebase_id_token = request.query_params.get('firebase_id_token')
        email = request.data.get('email')
        username = request.data.get('username')
        
        if (False):#email is None or firebase_id_token is None or username is None:
            return invalidResponse
        if(True):# is_admin(firebase_id_token):
            try:
                random_password = secrets.token_urlsafe(16)
                new_firebase_user = auth.create_user(email=email, password=random_password)
                new_andy_user = {
                    'uid': new_firebase_user.uid,
                    'username': username,
                    'email': email,
                    'created': datetime.now(),
                    'profile_img': '',
                    'is_staff': False,
                }
                serializer = self.get_serializer(data=new_andy_user)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except auth.EmailAlreadyExistsError:
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return invalidResponse
        else:
            return unauthorizedResponse
            
    #   update any user if admin, update self if not admin
    @action(detail=False, methods=['put', 'patch'], url_path='update_by_uid')
    def update_by_uid(self, request):
        uid = request.query_params.get('uid')
        firebase_id_token = request.query_params.get('firebase_id_token')
        
        if uid is None or firebase_id_token is None:
            return invalidResponse
        user = StockTrackUser.objects.get(uid=uid)
        decoded_token = auth.verify_id_token(firebase_id_token)
        decoded_uid = decoded_token['uid']
        try:
            if firebaseauth.is_admin(firebase_id_token):
                serializer = self.get_serializer(user, data=request.data, partial=True)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()    
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                if decoded_uid != uid or decoded_uid is None:
                    return unauthorizedResponse
                
                # only allow non admin user to edit their username and profile_img
                user_data = request.data.copy()
                user_data.pop('is_staff', None)
                user_data.pop('uid', None)
                user_data.pop('created', None)
                user_data.pop('email', None)
                
                serializer = self.get_serializer(user, data=user_data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
        except StockTrackUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except auth.InvalidIdTokenError:
            return Response({'error': 'Invalid Firebase ID token'}, status=status.HTTP_401_UNAUTHORIZED)

    #raw creation of a database user    
    def create(self, request):
        firebase_id_token = request.query_params.get('firebase_id_token')
        if firebaseauth.is_admin(firebase_id_token):
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return unauthorizedResponse
        
    #delete user by uid
    @action(detail=False, methods=['delete'], url_path='delete_by_uid')
    def delete_by_uid(self, request):
        uid = request.query_params.get('uid')
        firebase_id_token = request.query_params.get('firebase_id_token')
        
        if uid is None or firebase_id_token is None:
            return invalidResponse
        users = self.queryset.filter(uid=uid)
        if users.exists():
            if firebaseauth.is_admin(firebase_id_token):
                users.delete()
                auth.delete_user(uid=uid)
                return Response({'message': 'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return unauthorizedResponse
        else:
            return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    
    @action(detail=False, methods=['get'], url_path='retrieve_from_uid')
    def retrieve_from_uid(self, request):
        #query params
        uid = request.query_params.get('uid')
        firebase_id_token = request.query_params.get('firebase_id_token')
        
        if uid is None or firebase_id_token is None:
            return invalidResponse
        
        try:
            decoded_token = auth.verify_id_token(firebase_id_token)
            user = StockTrackUser.objects.get(uid=uid)
            user_data = self.get_serializer(user).data
            decoded_uid = decoded_token['uid']
            
            if not isAdmin(firebase_id_token):
                if decoded_uid != uid or decoded_uid is None:
                    return unauthorizedResponse
            return Response(user_data, status=status.HTTP_200_OK)
        except StockTrackUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except auth.InvalidIdTokenError:
            return Response({'error': 'Invalid Firebase ID token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    