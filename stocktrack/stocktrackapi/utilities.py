from rest_framework.response import Response
from rest_framework import status

UNAUTHORIZED = Response({'error': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
FORBIDDEN = Response({'error' : 'Forbidden content'}, status=status.HTTP_403_FORBIDDEN)
INVALID = Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
BAD_PAYLOAD = Response({'error': 'Bad payload'}, status=status.HTTP_400_BAD_REQUEST)
SERVER_ERROR = Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
SERVICE_UNAVAILABLE = Response({'error': 'Service temporarily unavailable'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

def created_response(data):
    return Response(data, status=status.HTTP_201_CREATED)

def success_response(message):
    return Response({'message': message}, status=status.HTTP_200_OK)

def bad_request_response(message):
    return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)