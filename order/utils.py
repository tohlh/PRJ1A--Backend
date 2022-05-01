import requests
from time import time
from driver.models import *
from passenger.models import *
from order.models import *
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from math import radians, cos, sin, asin, sqrt


BAIDU_APP_KEY = 'XnfPPmndtYGWtZ8869ECQKOuks4p89P4'


def getPOI(latitude, longitude):
    params = {
        'ak': BAIDU_APP_KEY,
        'output': 'json',
        'coordtype': 'gcj02ll',
        'ret_coordtype': 'gcj02ll',
        'extensions_poi': 5,
        'location': f'{latitude},{longitude}',
    }
    response = requests.get(
        "https://api.map.baidu.com/reverse_geocoding/v3/",
        params=params
    ).json()
    return response['result']['pois'][0]['name'], \
        response['result']['pois'][0]['addr']


def get_direction(lat_1, long_1, lat_2, long_2):
    params = {
        'ak': BAIDU_APP_KEY,
        'coord_type': 'gcj02',
        'ret_coordtype': 'gcj02',
        'origin': f'{lat_1},{long_1}',
        'destination': f'{lat_2},{long_2}',
    }
    response = requests.get(
        "https://api.map.baidu.com/direction/v2/driving",
        params=params
    ).json()

    routes = response['result']['routes'][0]['steps']
    distance = response['result']['routes'][0]['distance'] / 1000

    combined_route = []
    for route in routes:
        path = route['path']
        coords = path.split(';')
        for coord in coords:
            longitude, latitude = coord.split(',')
            combined_route.append({
                'latitude': float(latitude),
                'longitude': float(longitude)
            })

    return combined_route, distance


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


def pending_passenger_orders():
    ret = Order.objects.filter(status=0)
    return ret


def pending_drivers():
    time_threshold = timezone.now() - timedelta(minutes=1)
    ret = Driver.objects.filter(
        ~Q(username=''),
        ~Q(age=None),
        ~Q(identification_no=''),
        ~Q(carplate=''),
        ~Q(phone=''),
        last_online__gt=time_threshold
    )
    return ret


def match_orders():
    orders = pending_passenger_orders()
    drivers = pending_drivers()

    for order in orders:
        for driver in drivers:
            order_lat = order.start_POI_lat
            order_long = order.start_POI_long
            driver_lat = driver.latitude
            driver_long = driver.longitude
            dist_between = calc_distance(order_lat, order_long,
                                         driver_lat, driver_long)

            if dist_between <= 15:
                Order.objects.filter(id=order.id).update(
                    driver=driver,
                    status=1
                )
                break
