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
    if driver_unregistered(driver_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })
    return payload_response({})


@api_view(('POST',))
def DriverUpdateLocationView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)
    if driver_unregistered(driver_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

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
    if driver_unregistered(driver_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    if not current_order_exists(driver_id):
        return payload_response({})

    current_order = get_current_order(driver_id)
    current_order.distance = calc_distance(
        current_order.start_POI_lat,
        current_order.start_POI_long,
        current_order.end_POI_lat,
        current_order.end_POI_long
    )
    serializer = DriverOngoingOrderSerializer(current_order)
    return payload_response(serializer.data)


@api_view(('POST',))
def DriverPickupPassengerView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)
    if driver_unregistered(driver_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    if not current_order_exists(driver_id):
        return bad_request_response({
            'errMsg': '您目前没有接到订单。'
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
    if driver_unregistered(driver_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    if not current_order_exists(driver_id):
        return bad_request_response({
            'errMsg': '您目前没有接到订单。'
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
    if driver_unregistered(driver_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    if not current_order_exists(driver_id):
        return bad_request_response({
            'errMsg': '您目前没有接到订单。'
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
    if driver_unregistered(driver_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 10))

    orders = Order.objects.filter(
        Q(status=3) | Q(status=4) | Q(status=6),
        driver__id=driver_id
    ).order_by('-created_at')
    orders = orders[offset:offset+limit]
    serializer = DriverCompletedOrderSerializer(
        orders,
        many=True
    )
    return payload_response(serializer.data)


@api_view(('GET',))
def DriverCurrentOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)
    if driver_unregistered(driver_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    if not current_order_exists(driver_id):
        return payload_response({
            'status': -1
        })

    if current_order_exists(driver_id):
        current_order = get_current_order(driver_id)
        return payload_response({
            'status': current_order.status,
            'price': current_order.real_price,
            'distance': current_order.distance
        })
