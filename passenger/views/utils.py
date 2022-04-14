import jwt
from prj1a.settings import SIMPLE_JWT
from rest_framework.response import Response
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


# Orders
def pending_order_exists(passenger_id):
    time_threshold = timezone.now() - timedelta(minutes=2)
    pending_order = Order.objects.filter(
        Q(status=0) | Q(status=1),
        passenger__id=passenger_id,
        updated_at__gt=time_threshold
    )
    return pending_order.exists()


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
