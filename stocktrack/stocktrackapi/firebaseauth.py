from django.http import JsonResponse
from firebase_admin import auth
from stocktrackapi.models.stocktrackuser import StockTrackUser
    
# Return user's role
def get_user_role(firebase_token):
    if not firebase_token:
        return None
    
    try:
        decoded_token = auth.verify_id_token(firebase_token)
        decoded_uid = decoded_token['uid']
        try:
            user = StockTrackUser.objects.get(uid=decoded_uid)
            return user.role
        except StockTrackUser.DoesNotExist:
            print(f"User with UID {decoded_uid} does not exist")
            return None
    except auth.InvalidIdTokenError:
        return None
    
def get_decoded_token(firebase_token):
    if firebase_token is None:
        return None
    
    try:
        print("Verifying id token...")
        decoded_token = auth.verify_id_token(firebase_token)
        print(f"Id token verified. User is {decoded_token['email']}")
        return decoded_token
    except auth.InvalidIdTokenError:
        print("Invalid id token")
        return None