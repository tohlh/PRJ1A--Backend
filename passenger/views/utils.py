import jwt
import json
import base64
import math
from prj1a.settings import SIMPLE_JWT
from rest_framework.response import Response
from passenger.models import Passenger
from datetime import timedelta
from django.utils import timezone
from order.models import Order
from django.db.models import Q


# Passenger Authentication
def decode_passenger_token(request):
    encoded_token = request.META.get('HTTP_AUTHORIZATION')[7:]
    decoded_token = jwt.decode(encoded_token,
                               SIMPLE_JWT['SIGNING_KEY'],
                               algorithms=[SIMPLE_JWT['ALGORITHM']])
    return decoded_token


def is_passenger(request):
    decoded_token = decode_passenger_token(request)
    return decoded_token['type'] == 'passenger'


def get_passenger_id(request):
    decoded_token = decode_passenger_token(request)
    return decoded_token['user_id']


def passenger_unregistered(passenger_id):
    passenger_object = Passenger.objects.get(id=passenger_id)
    if passenger_object.username == '' or \
       passenger_object.phone == '' or \
       passenger_object.identification_no == '' or \
       passenger_object.age is None:
        return True
    return False


# Orders
def pending_order_exists(passenger_id):
    pending_order = Order.objects.filter(
        status=0,
        passenger__id=passenger_id
    )
    return pending_order.exists()


def current_order_exists(passenger_id):
    ret = Order.objects.filter(
        Q(status=1) | Q(status=2),
        passenger__id=passenger_id,
    )
    return ret.exists()


def unpaid_order_exists(passenger_id):
    return Order.objects.filter(
        status=5,
        passenger__id=passenger_id,
    ).exists()


def get_current_order(passenger_id):
    ret = Order.objects.filter(
        status=0,
        passenger__id=passenger_id,
    )
    if ret.exists():
        return ret.first()

    ret = Order.objects.filter(
        status=1,
        passenger__id=passenger_id,
    )
    if ret.exists():
        return ret.first()

    ret = Order.objects.filter(
        status=2,
        passenger__id=passenger_id,
    )
    if ret.exists():
        return ret.first()


def get_unpaid_order(passenger_id):
    ret = Order.objects.filter(
        status=5,
        passenger__id=passenger_id,
    )
    if ret.exists():
        return ret.first()


def current_driver_rotation(passenger_id):
    current_order = get_current_order(passenger_id)
    decoded_json_string = base64.b64decode(
        current_order.before_pickup_path
    )

    points = {}
    if current_order.status == 1:
        points = json.loads(decoded_json_string)
    elif current_order.status == 2:
        points = json.loads(decoded_json_string)

    if len(points) <= 1:
        return 0

    point_1 = points[-1]
    point_2 = points[-2]
    x = point_1['longitude'] - point_2['longitude']
    x = x / point_1['latitude'] - point_2['latitude']
    return math.atan(x)


# Http Responses
def payload_response(payload):
    return Response(payload, 200)


def bad_request_response(payload):
    return Response(payload, 400)


def unregistered_response(payload):
    return Response(payload, 402)


def unauthorized_response():
    return Response({
            'response': 'You are not authorized to access this API'
        }, 401)


def internal_error_response():
    return Response({
        'response': 'There is an error'
    }, 500)
