from lib2to3.pgen2 import driver
from driver.models import *
from driver.views.utils import *
from driver.serializers import *
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


@api_view(('POST',))
def DriverQueueOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)
    return payload_response({})


@api_view(('POST',))
def DriverUpdateLocationView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    latitude = request.data['latitude']
    longitude = request.data['longitude']

    Driver.objects.filter(
        id=driver_id
    ).update(
        latitude=latitude,
        longitude=longitude,
        last_online=timezone.now()
    )

    if not current_order_exists(driver_id):
        return payload_response({})

    current_order = get_current_order(driver_id)
    passenger_lat = current_order.passenger.latitude
    passenger_long = current_order.passenger.longitude
    return payload_response({
        'latitude': passenger_lat,
        'longitude': passenger_long
    })
