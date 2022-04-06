from base64 import decode
import jwt
from .models import Driver
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


def is_valid_driver(request):
    decoded_token = decode_user_token(request)
    if decoded_token['type'] == 'driver':
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
def DriverInfoView(request):
    permission_classes = (IsAuthenticated,)
    if not is_valid_driver(request):
        return unauthorized_response()
    decoded_token = decode_user_token(request)
    driver_id = decoded_token['user_id']

    def driver_info_response(driver_id):
        driver_object = Driver.objects.get(id=driver_id)
        payload = {
            'username': driver_object.username,
            'carplate': driver_object.carplate,
        }
        return Response(payload, 200)

    if request.method == 'GET':
        return driver_info_response(driver_id)
    elif request.method == 'POST':
        Driver.objects.filter(id=driver_id).update(
            username=request.data['username'],
            carplate=request.data['carplate']
        )
        return driver_info_response(driver_id)

    return internal_error_response()
