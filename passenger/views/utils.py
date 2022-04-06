import jwt
from prj1a.settings import SIMPLE_JWT
from rest_framework.response import Response

"""
Passenger Authentication
"""
def decode_user_token(request):
    encoded_token = request.META.get('HTTP_AUTHORIZATION')[7:]
    decoded_token = jwt.decode(encoded_token,
                               SIMPLE_JWT['SIGNING_KEY'],
                               algorithms=[SIMPLE_JWT['ALGORITHM']])
    return decoded_token


def is_authorized(request):
    decoded_token = decode_user_token(request)
    if decoded_token['type'] == 'passenger':
        return True
    return False


def get_passenger_id(request):
    decoded_token = decode_user_token(request)
    return decoded_token['user_id']

"""
Http Responses
"""
def payload_response(payload):
    return Response(payload, 200)


def unauthorized_response():
    return Response({
            'response': 'You are not authorized to access this API'
        }, 401)


def internal_error_response():
    return Response({
        'response': 'There is an error'
    }, 500)