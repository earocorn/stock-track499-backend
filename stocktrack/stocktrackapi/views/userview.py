from datetime import datetime
import secrets
from rest_framework import viewsets
from rest_framework.decorators import action, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from ..models.stocktrackuser import StockTrackUser, Role
from ..serializers import StockTrackUserSerializer
from .. import firebaseauth
from .. import utilities

from firebase_admin import auth


# Add user
# Add inventory
# Add order

# /stocktrackusers

class StockTrackUserViewSet(viewsets.GenericViewSet):
    queryset = StockTrackUser.objects.all().order_by('created')
    serializer_class = StockTrackUserSerializer

    # Create new user
    # Be able to create your own database user with your own token, or if you are admin/manager, create user for another person.
    def create(self, request):
        firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
        email = request.data.get('email')
        username = request.data.get('username')
        requested_role = request.data.get('role', Role.CUSTOMER)
        print(f"Email: {email}")
        print(f"Username: {username}")
        print(f"Requested Role: {requested_role}")

        if email is None or firebase_token is None or username is None:
            return utilities.BAD_PAYLOAD
        
        # Get request user's role
        role_from_token = firebaseauth.get_user_role(firebase_token)

        # Invalid role = customer
        if not Role.is_valid(role_from_token):
            requested_role = Role.CUSTOMER

        # Don't allow lower level user to get higher level role
        has_permissions = Role.is_admin_or_manager(role_from_token)
        if not has_permissions and requested_role != Role.CUSTOMER:
            return utilities.FORBIDDEN
        
        try:
            # Admin/Manager creating account for someone
            if has_permissions:
                print("User has permissions, creating new account")
                random_password = secrets.token_urlsafe(16)
                new_firebase_user = auth.create_user(email=email, password='password123')
                print(new_firebase_user)
                uid = new_firebase_user.uid
            # Customer creating their own account
            else:
                print("User does not have permissions, creating own account")
                decoded_token = firebaseauth.get_decoded_token(firebase_token)
                if not decoded_token:
                    return utilities.FORBIDDEN
                uid = decoded_token['uid']
                print('decoded', decoded_token)
            
            new_user = {
                'uid': uid,
                'username': username,
                'email': email,
                'created': datetime.now(),
                'profile_img': '',
                'role': Role.CUSTOMER
            }
            print('Attempting to create user', new_user)

            # Save user in database
            serializer = self.get_serializer(data=new_user)

            if not serializer.is_valid():
                print('serializer errors', serializer.errors)
                print('User data invalid; unable to serialize')
                return utilities.SERVER_ERROR
            
            serializer.save()
            return utilities.created_response(data=new_user)
        
        except auth.EmailAlreadyExistsError:
            return utilities.bad_request_response("Email already exists")
        
        except Exception as e:
            print(str(e.with_traceback(None)))
            return utilities.SERVER_ERROR
        

    def list(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if not auth_header:
                return utilities.UNAUTHORIZED

            firebase_token = auth_header.split()[1]
            role_from_token = firebaseauth.get_user_role(firebase_token)
            print(role_from_token)

            # Only allow admins/managers to see all users
#             if not Role.is_admin_or_manager(role_from_token):
#                 return utilities.UNAUTHORIZED

            serializer = self.get_serializer(self.queryset, many=True)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
    # Retrieve yourself, or retrieve anyone if admin/manager
    def retrieve(self, request, pk=None):
        firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
        if not firebase_token:
            return utilities.UNAUTHORIZED
        role_from_token = firebaseauth.get_user_role(firebase_token)
        
        try:
            decoded_token = firebaseauth.get_decoded_token(firebase_token)
            if not decoded_token:
                return utilities.INVALID
            decoded_uid = decoded_token['uid']

            # Only allow admins/managers to see any user, or allow user to see themself
            if not Role.is_admin_or_manager(role_from_token) and decoded_uid != pk:
                return utilities.FORBIDDEN
            
            user = StockTrackUser.objects.get(uid=pk) 
            serializer = self.get_serializer(user)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StockTrackUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except auth.InvalidIdTokenError:
            return Response({'error': 'Invalid Firebase ID token'}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
        if not firebase_token:
            return utilities.UNAUTHORIZED
        role_from_token = firebaseauth.get_user_role(firebase_token)
        
        try:
            decoded_token = firebaseauth.get_decoded_token(firebase_token)
            if not decoded_token:
                return utilities.INVALID
            decoded_uid = decoded_token['uid']

            # Allow admins/managers to update any user or regular users to update themselves
            if not Role.is_admin_or_manager(role_from_token) and decoded_uid != pk:
                return utilities.FORBIDDEN

            user = StockTrackUser.objects.get(uid=pk)

            # Admins/managers can update any field; regular users are restricted
            if not Role.is_admin_or_manager(role_from_token):
                restricted_fields = ['role', 'email', 'created']
                user_data = request.data.copy()
                for field in restricted_fields:
                    user_data.pop(field, None)
            else:
                user_data = request.data

            serializer = self.get_serializer(user, data=user_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return utilities.success_response("User successfully updated")
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except StockTrackUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except auth.InvalidIdTokenError:
            return Response({'error': 'Invalid Firebase ID token'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(str(e))
            return utilities.SERVER_ERROR

    def destroy(self, request, pk=None):
        firebase_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
        if not firebase_token:
            return utilities.UNAUTHORIZED
        role_from_token = firebaseauth.get_user_role(firebase_token)
        
        try:
            decoded_token = firebaseauth.get_decoded_token(firebase_token)
            if not decoded_token:
                return utilities.INVALID
            decoded_uid = decoded_token['uid']

            # Only allow admins/managers to see any user, or allow user to see themself
            if not Role.is_admin_or_manager(role_from_token) and decoded_uid != pk:
                return utilities.FORBIDDEN
            
            user = StockTrackUser.objects.get(uid=pk) 
            user.delete()
            auth.delete_user(uid=pk)
            
            return utilities.success_response("Successfully deleted user")
        except StockTrackUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except auth.InvalidIdTokenError:
            return Response({'error': 'Invalid Firebase ID token'}, status=status.HTTP_401_UNAUTHORIZED)
            
    # #   update any user if admin, update self if not admin
    # @action(detail=False, methods=['put', 'patch'], url_path='update_by_uid')
    # def update_by_uid(self, request):
    #     uid = request.query_params.get('uid')
    #     firebase_id_token = request.query_params.get('firebase_id_token')
        
    #     if uid is None or firebase_id_token is None:
    #         return utilities.BAD_PAYLOAD
    #     user = StockTrackUser.objects.get(uid=uid)
    #     decoded_token = auth.verify_id_token(firebase_id_token)
    #     decoded_uid = decoded_token['uid']
    #     try:
    #         if firebaseauth.is_admin(firebase_id_token):
    #             serializer = self.get_serializer(user, data=request.data, partial=True)
    #             if not serializer.is_valid():
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #             serializer.save()    
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         else:
    #             if decoded_uid != uid or decoded_uid is None:
    #                 return unauthorizedResponse
                
    #             # only allow non admin user to edit their username and profile_img
    #             user_data = request.data.copy()
    #             user_data.pop('is_staff', None)
    #             user_data.pop('uid', None)
    #             user_data.pop('created', None)
    #             user_data.pop('email', None)
                
    #             serializer = self.get_serializer(user, data=user_data, partial=True)
    #             serializer.is_valid(raise_exception=True)
    #             serializer.save()
                
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #     except StockTrackUser.DoesNotExist:
    #         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except auth.InvalidIdTokenError:
    #         return Response({'error': 'Invalid Firebase ID token'}, status=status.HTTP_401_UNAUTHORIZED)
