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

    data = request.data
    lat_1 = float(request.data['start']['latitude'])
    long_1 = float(request.data['start']['longitude'])
    lat_2 = float(request.data['end']['latitude'])
    long_2 = float(request.data['end']['longitude'])

    payload = {
        'points': [
            {
                'address': data['start']['address'],
                'name': data['start']['name'],
                'latitude': lat_1,
                'longitude': long_1,
            },
            {
                'address': data['end']['address'],
                'name': data['end']['name'],
                'latitude': lat_2,
                'longitude': long_2,
            }
        ],
        'distance': calc_distance(lat_1, long_1, lat_2, long_2),
        'price': est_price(lat_1, long_1, lat_2, long_2)
    }
    return payload_response(payload)


@api_view(('POST',))
def PassengerNewOrderView(request):
    # Places an order and record the order into the database
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if pending_order_exists(passenger_id) or \
       current_order_exists(passenger_id):
        return bad_request_response({})

    data = request.data
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
        est_price=est_price(
            float(data['start']['latitude']),
            float(data['start']['longitude']),
            float(data['end']['latitude']),
            float(data['end']['longitude'])
        ),
        updated_at=timezone.now(),
        status=0
    )

    Passenger.objects.filter(
        id=passenger_id
    ).update(
        latitude=float(data['start']['latitude']),
        longitude=float(data['start']['longitude'])
    )
    match_orders()

    return payload_response({})


@api_view(('GET',))
def PassengerCurrentOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if not (pending_order_exists(passenger_id) or
            current_order_exists(passenger_id)):
        return payload_response(None)

    order = get_current_order(passenger_id)
    serializer = PassengerOrderSerializer(order)
    return payload_response(serializer.data)


@api_view(('POST',))
def PassengerCancelOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if not (pending_order_exists(passenger_id) or
            current_order_exists(passenger_id)):
        return bad_request_response({})

    cancel_current_order(passenger_id)
    return payload_response({})


@api_view(('POST',))
def PassengerUpdateLocationView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if not (pending_order_exists(passenger_id) or
            current_order_exists(passenger_id)):
        return bad_request_response({})

    data = request.data
    keys = ['latitude', 'longitude']
    for key in keys:
        if key not in data:
            return bad_request_response(f'\'{key}\' is required')

    update_current_order(passenger_id)
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
        'longitude': driver.longitude
    }
    return payload_response(response)


@api_view(('GET',))
def PassengerListOrdersView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 10))

    orders = Order.objects.filter(
        passenger__id=passenger_id
    ).order_by('-created_at')
    orders = orders[offset:offset+limit]
    serializer = PassengerOrderSerializer(
        orders,
        many=True
    )
    return payload_response(serializer.data)
