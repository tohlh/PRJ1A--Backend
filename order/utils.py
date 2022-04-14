from time import time
from driver.models import *
from passenger.models import *
from order.models import *
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from math import radians, cos, sin, asin, sqrt


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


def pending_passenger_orders():
    time_threshold = timezone.now() - timedelta(minutes=2)
    ret = Order.objects.filter(
        status=0,
        updated_at__gt=time_threshold
    )
    return ret


def pending_drivers():
    time_threshold = timezone.now() - timedelta(minutes=1)
    ret = Driver.objects.filter(
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
                Order.objects.filter(id=order.id).update(driver=driver)
                break
