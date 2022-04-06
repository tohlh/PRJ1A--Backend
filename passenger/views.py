import jwt
from .models import Passenger
from prj1a.settings import SIMPLE_JWT
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def decode_user_token(request):
    encoded_token = request.META.get('HTTP_AUTHORIZATION')[7:]
    decoded_token = jwt.decode(encoded_token,
                               SIMPLE_JWT['SIGNING_KEY'],
                               algorithms=[SIMPLE_JWT['ALGORITHM']])
    return decoded_token


def is_valid_passenger(request):
    decoded_token = decode_user_token(request)
    if decoded_token['type'] == 'passenger':
        return True
    else:
        return False


def unauthorized_response():
    return Response({
            'response': 'You are not authorized to access this API'
        }, 401)


def internal_error_response():
    return Response({
        'response': 'There is an error'
    }, 500)


@api_view(('GET', 'POST'))
def PassengerInfoView(request):
    permission_classes = (IsAuthenticated,)
    if not is_valid_passenger(request):
        return unauthorized_response()
    decoded_token = decode_user_token(request)
    passenger_id = decoded_token['user_id']

    def passenger_info_response(passenger_id):
        passenger_object = Passenger.objects.get(id=passenger_id)
        payload = {
            'username': passenger_object.username,
        }
        return Response(payload, 200)

    if request.method == 'GET':
        return passenger_info_response(passenger_id)
    elif request.method == 'POST':
        Passenger.objects.filter(id=passenger_id).update(
            username=request.data['username'],
        )
        return passenger_info_response(passenger_id)

    return internal_error_response()
