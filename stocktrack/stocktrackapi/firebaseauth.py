from django.http import JsonResponse
from firebase_admin import auth
from stocktrackapi.models.stocktrackuser import StockTrackUser

# Return if user is admin
def is_admin(firebase_id_token):
    if firebase_id_token is None:
        return False

    try:
        decoded_token = auth.verify_id_token(firebase_id_token)
        decoded_uid = decoded_token['uid']
        user = StockTrackUser.objects.get(uid=decoded_uid)
        if user:
            if user.is_staff == True:
                return True
        return False
        
    except auth.InvalidIdTokenError:
        return False
    
# Return user's role
def get_role(firebase_id_token):
    pass