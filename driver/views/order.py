import driver
from driver.models import *
from driver.views.utils import *
from driver.serializers import *
from order.utils import *
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
    match_orders()
    record_path(driver_id, latitude, longitude)

    if current_order_exists(driver_id):
        current_order = get_current_order(driver_id)
        passenger = current_order.passenger
        return payload_response({
            'latitude': passenger.latitude,
            'longitude': passenger.longitude
        })

    return payload_response({})


@api_view(('GET',))
def DriverGetOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    if not current_order_exists(driver_id):
        return payload_response({})

    current_order = get_current_order(driver_id)
    serializer = DriverOrderSerializer(current_order)
    return payload_response(serializer.data)


@api_view(('POST',))
def DriverPickupPassengerView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    if not current_order_exists(driver_id):
        return bad_request_response({
            'errMsg': 'You do not have an active order.'
        })

    current_order = get_current_order(driver_id)
    Order.objects.filter(
        id=current_order.id
    ).update(
        status=2
    )
    return payload_response({})


@api_view(('POST',))
def DriverCancelOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    if not current_order_exists(driver_id):
        return bad_request_response({
            'errMsg': 'You do not have an active order.'
        })

    current_order = get_current_order(driver_id)
    Order.objects.filter(
        id=current_order.id
    ).update(
        status=4
    )
    return payload_response({})


@api_view(('POST',))
def DriverEndOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    if not current_order_exists(driver_id):
        return bad_request_response({
            'errMsg': 'You do not have an active order.'
        })

    current_order = get_current_order(driver_id)
    Order.objects.filter(
        id=current_order.id
    ).update(
        status=5,
        ended_at=timezone.now()
    )
    return payload_response({})


@api_view(('GET',))
def DriverListOrdersView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 10))

    orders = Order.objects.filter(
        driver__id=driver_id
    ).order_by('-ended_at')
    orders = orders[offset:offset+limit]
    serializer = DriverOrderSerializer(
        orders,
        many=True
    )
    return payload_response(serializer.data)
