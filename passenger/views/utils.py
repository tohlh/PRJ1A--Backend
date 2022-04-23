import jwt
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
    time_threshold = timezone.now() - timedelta(minutes=2)
    pending_order = Order.objects.filter(
        status=0,
        passenger__id=passenger_id,
        updated_at__gt=time_threshold
    )
    return pending_order.exists()


def current_order_exists(passenger_id):
    time_threshold = timezone.now() - timedelta(minutes=2)
    ret1 = Order.objects.filter(
        status=1,
        passenger__id=passenger_id,
        updated_at__gt=time_threshold
    )
    ret2 = Order.objects.filter(
        status=2,
        passenger__id=passenger_id,
    )
    return ret1 or ret2


def get_current_order(passenger_id):
    time_threshold = timezone.now() - timedelta(minutes=2)
    ret = Order.objects.filter(
        status=0,
        passenger__id=passenger_id,
        updated_at__gt=time_threshold
    )
    if ret.exists():
        return ret.first()

    time_threshold = timezone.now() - timedelta(minutes=2)
    ret = Order.objects.filter(
        status=1,
        passenger__id=passenger_id,
        updated_at__gt=time_threshold
    )
    if ret.exists():
        return ret.first()

    time_threshold = timezone.now() - timedelta(minutes=2)
    ret = Order.objects.filter(
        status=2,
        passenger__id=passenger_id,
    )
    if ret.exists():
        return ret.first()


def cancel_current_order(passenger_id):
    time_threshold = timezone.now() - timedelta(minutes=2)
    Order.objects.filter(
        Q(status=0) | Q(status=1),
        passenger__id=passenger_id,
        updated_at__gt=time_threshold
    ).update(status=3)

    Order.objects.filter(
        status=2,
        passenger__id=passenger_id,
    ).update(status=3)


def update_current_order(passenger_id):
    time_threshold = timezone.now() - timedelta(minutes=2)
    pending_order = Order.objects.filter(
        Q(status=0) | Q(status=1),
        passenger__id=passenger_id,
        updated_at__gt=time_threshold
    ).update(updated_at=timezone.now())


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
