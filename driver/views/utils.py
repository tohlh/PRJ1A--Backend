import jwt
import decimal
from django.db.models import Q
from prj1a.settings import SIMPLE_JWT
from rest_framework.response import Response
from order.models import Order
from order.utils import *


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


def driver_unregistered(driver_id):
    driver_object = Driver.objects.get(id=driver_id)
    if driver_object.username == '' or \
       driver_object.phone == '' or \
       driver_object.identification_no == '' or \
       driver_object.age is None:
        return True
    return False


# Order
def current_order_exists(driver_id):
    current_order = Order.objects.filter(
        Q(status=1) | Q(status=2),
        driver__id=driver_id
    )
    return current_order.exists()


def get_current_order(driver_id):
    current_order = Order.objects.get(
        Q(status=1) | Q(status=2),
        driver__id=driver_id
    )
    return current_order


def record_path(driver_id, latitude, longitude):
    if not current_order_exists(driver_id):
        return

    current_order = get_current_order(driver_id)
    new_entry = {
        'latitude': float(latitude),
        'longitude': float(longitude)
    }
    if current_order.status == 1:
        path_list = current_order.before_pickup_path
        if path_list == '':
            path_list = dict_list_to_base64_json([])
        path_list = base64_json_to_dict_list(path_list)
        path_list.append(new_entry)
        encoded_path = dict_list_to_base64_json(path_list)
        Order.objects.filter(
            id=current_order.id
        ).update(
            before_pickup_path=encoded_path
        )
    elif current_order.status == 2:
        path_list = current_order.after_pickup_path
        if path_list == '':
            path_list = dict_list_to_base64_json([])
        path_list = base64_json_to_dict_list(path_list)

        new_distance = 0
        if len(path_list) != 0:
            new_distance = calc_distance(
                path_list[-1]['latitude'],
                path_list[-1]['longitude'],
                new_entry['latitude'],
                new_entry['longitude']
            ) + current_order.distance

        new_price = new_distance * 5
        new_price = str(round(new_price, 2))
        new_price = decimal.Decimal(new_price)

        path_list.append(new_entry)
        encoded_path = dict_list_to_base64_json(path_list)
        Order.objects.filter(
            id=current_order.id
        ).update(
            after_pickup_path=encoded_path,
            distance=new_distance,
            real_price=new_price
        )


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
