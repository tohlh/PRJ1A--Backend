import jwt
from prj1a.settings import SIMPLE_JWT
from rest_framework.response import Response
from order.models import Order
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q


# Driver Authentication
def decode_driver_token(request):
    encoded_token = request.META.get('HTTP_AUTHORIZATION')[7:]
    decoded_token = jwt.decode(encoded_token,
                               SIMPLE_JWT['SIGNING_KEY'],
                               algorithms=[SIMPLE_JWT['ALGORITHM']])
    return decoded_token


def is_driver(request):
    decoded_token = decode_driver_token(request)
    if decoded_token['type'] == 'driver':
        return True
    return False


def get_driver_id(request):
    decoded_token = decode_driver_token(request)
    return decoded_token['user_id']


# Order
def current_order_exists(driver_id):
    time_threshold = timezone.now() - timedelta(minutes=2)
    criteria = (Q(driver__id=driver_id) & Q(status=1) &
                Q(updated_at__gt=time_threshold)) | Q(status=2)
    current_order = Order.objects.filter(criteria)
    return current_order.exists()


def get_current_order(driver_id):
    time_threshold = timezone.now() - timedelta(minutes=2)
    criteria = (Q(driver__id=driver_id) & Q(status=1) &
                Q(updated_at__gt=time_threshold)) | Q(status=2)
    current_order = Order.objects.get(criteria)
    return current_order


# Http Responses
def payload_response(payload):
    return Response(payload, 200)


def bad_request_response(payload):
    return Response(payload, 400)


def unauthorized_response():
    return Response({
            'response': 'You are not authorized to access this API'
        }, 401)


def internal_error_response():
    return Response({
        'response': 'There is an error'
    }, 500)
