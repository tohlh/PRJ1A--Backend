from passenger.models import *
from passenger.views.utils import *
from passenger.serializers import *
from order.utils import *
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


@api_view(('POST',))
def PassengerEstimatePriceView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if passenger_unregistered(passenger_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    data = request.data

    if data['start']['name'] == '' or data['start']['address'] == '':
        data['start']['name'], data['start']['address'] = \
            getPOI(data['start']['latitude'],
                   data['start']['longitude'])

    if data['end']['name'] == '' or data['end']['address'] == '':
        data['end']['name'], data['end']['address'] = \
            getPOI(data['end']['latitude'],
                   data['end']['longitude'])

    lat_1 = float(request.data['start']['latitude'])
    long_1 = float(request.data['start']['longitude'])
    lat_2 = float(request.data['end']['latitude'])
    long_2 = float(request.data['end']['longitude'])

    points, distance = get_direction(lat_1, long_1, lat_2, long_2)
    payload = {
        'points': points,
        'distance': distance,
        'price': round(distance * 6, 2)
    }
    return payload_response(payload)


@api_view(('POST',))
def PassengerNewOrderView(request):
    # Places an order and record the order into the database
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if passenger_unregistered(passenger_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    if Order.objects.filter(
        passenger__id=passenger_id,
        status=5
    ).exists():
        return bad_request_response({
            'errMsg': '请支付未付款的订单。'
        })

    if pending_order_exists(passenger_id) or \
       current_order_exists(passenger_id):
        return bad_request_response({
            'errMsg': '您已经下单了。'
        })

    passenger = Passenger.objects.get(id=passenger_id)
    if passenger.latitude == '' or passenger.longitude == '':
        return bad_request_response({
            'errMsg': '请更新您的位置。'
        })

    data = request.data

    if data['start']['name'] == '' or data['start']['address'] == '':
        data['start']['name'], data['start']['address'] = \
            getPOI(data['start']['latitude'],
                   data['start']['longitude'])

    if data['end']['name'] == '' or data['end']['address'] == '':
        data['end']['name'], data['end']['address'] = \
            getPOI(data['end']['latitude'],
                   data['end']['longitude'])

    Order.objects.create(
        passenger=Passenger.objects.get(id=passenger_id),
        start_POI_name=data['start']['name'],
        start_POI_address=data['start']['address'],
        start_POI_lat=float(data['start']['latitude']),
        start_POI_long=float(data['start']['longitude']),
        end_POI_name=data['end']['name'],
        end_POI_address=data['end']['address'],
        end_POI_lat=float(data['end']['latitude']),
        end_POI_long=float(data['end']['longitude']),
        est_price=100,
        status=0
    )

    match_orders()

    return payload_response({})


@api_view(('GET',))
def PassengerGetOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if passenger_unregistered(passenger_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    if unpaid_order_exists(passenger_id):
        unpaid_order = get_unpaid_order(passenger_id)
        serializer = PassengerOrderInfoSerializer(unpaid_order)
        return payload_response(serializer.data)

    if not (pending_order_exists(passenger_id) or
            current_order_exists(passenger_id)):
        return payload_response(None)

    order = get_current_order(passenger_id)
    serializer = PassengerOrderInfoSerializer(order)
    return payload_response(serializer.data)


@api_view(('POST',))
def PassengerCancelOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if passenger_unregistered(passenger_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    if not (pending_order_exists(passenger_id) or
            current_order_exists(passenger_id)):
        return bad_request_response({
            'errMsg': '您目前没有订单。'
        })

    current_order = get_current_order(passenger_id)
    if current_order.status >= 2:
        return bad_request_response({
            'errMsg': '当前阶段不允许取消订单。'
        })

    Order.objects.filter(
        Q(status=0) | Q(status=1) | Q(status=2),
        passenger__id=passenger_id,
    ).update(
        status=3,
        canceled_at=timezone.now()
    )

    return payload_response({})


@api_view(('POST',))
def PassengerUpdateLocationView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if passenger_unregistered(passenger_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    data = request.data
    keys = ['latitude', 'longitude']
    for key in keys:
        if key not in data:
            return bad_request_response(f'\'{key}\' is required')

    Passenger.objects.filter(
        id=passenger_id
    ).update(
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    match_orders()

    if not current_order_exists(passenger_id):
        return payload_response({})

    current_order = get_current_order(passenger_id)
    driver = current_order.driver
    response = {
        'latitude': driver.latitude,
        'longitude': driver.longitude,
        'rotate': current_driver_rotation(passenger_id)
    }
    return payload_response(response)


@api_view(('GET',))
def PassengerListOrdersView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if passenger_unregistered(passenger_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 10))

    orders = Order.objects.filter(
        Q(status=3) | Q(status=4) | Q(status=5) | Q(status=6),
        passenger__id=passenger_id
    ).order_by('-created_at')
    orders = orders[offset:offset+limit]
    serializer = PassengerOrderListSerializer(
        orders,
        many=True
    )
    return payload_response(serializer.data)


@api_view(('GET',))
def PassengerOrderDetailsView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if passenger_unregistered(passenger_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    id = int(request.GET.get('id', -1))
    if id == -1:
        return bad_request_response({
            'errMsg': '请提供订单 id'
        })

    order = Order.objects.get(id=id)
    serializer = PassengerOrderDetailSerializer(order)
    return payload_response(serializer.data)


@api_view(('GET',))
def PassengerCurrentOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if passenger_unregistered(passenger_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    if pending_order_exists(passenger_id):
        return payload_response({
            'status': 0
        })

    if current_order_exists(passenger_id):
        current_order = get_current_order(passenger_id)
        return payload_response({
            'status': current_order.status,
            'price': current_order.real_price,
            'distance': current_order.distance
        })

    if not (pending_order_exists(passenger_id) or
            current_order_exists(passenger_id)):
        if unpaid_order_exists(passenger_id):
            unpaid_order = get_unpaid_order(passenger_id)
            return payload_response({
                'status': 5,
                'price': unpaid_order.real_price,
                'distance': unpaid_order.distance
            })

    return payload_response({
        'status': -1
    })


@api_view(('POST',))
def PassengerPayOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if passenger_unregistered(passenger_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    Order.objects.filter(
        passenger__id=passenger_id,
        status=5
    ).update(
        status=6,
        paid_at=timezone.now()
    )
    return payload_response({})
