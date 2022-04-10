import jwt
from prj1a.settings import SIMPLE_JWT
from rest_framework.response import Response
from math import radians, cos, sin, asin, sqrt
from datetime import timedelta
from django.utils import timezone
from order.models import Order
from django.db.models import Q


# Passenger Authentication
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


# Orders
def pending_order_exists(passenger_id):
    time_threshold = timezone.now() - timedelta(minutes=2)
    pending_order = Order.objects.filter(
        Q(status=0) | Q(status=1),
        passenger__id=passenger_id,
        updated_at__gt=time_threshold
    )
    if pending_order.exists():
        return True
    else:
        return False


def get_current_order(passenger_id):
    time_threshold = timezone.now() - timedelta(minutes=2)
    pending_order = Order.objects.get(
        Q(status=0) | Q(status=1),
        passenger__id=passenger_id,
        updated_at__gt=time_threshold
    )
    return pending_order


def cancel_current_order(passenger_id):
    time_threshold = timezone.now() - timedelta(minutes=2)
    pending_order = Order.objects.filter(
        Q(status=0) | Q(status=1),
        passenger__id=passenger_id,
        updated_at__gt=time_threshold
    ).update(status=3)


def calc_distance(lat_1, long_1, lat_2, long_2):
    lat_1 = radians(lat_1)
    long_1 = radians(long_1)
    lat_2 = radians(lat_2)
    long_2 = radians(long_2)

    d_lat = lat_2 - lat_1
    d_long = long_2 - long_1
    a = sin(d_lat / 2)**2 + cos(lat_1) * cos(lat_2) * sin(d_long / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return(c * r)


def est_price(lat_1, long_1, lat_2, long_2):
    ret = 10 * calc_distance(lat_1, long_1, lat_2, long_2)
    ret = round(ret, 2)
    return ret


# Http Responses
def payload_response(payload):
    return Response(payload, 200)


def bad_request_response(message):
    return Response({
        'response': message
    }, 400)


def unauthorized_response():
    return Response({
            'response': 'You are not authorized to access this API'
        }, 401)


def internal_error_response():
    return Response({
        'response': 'There is an error'
    }, 500)
