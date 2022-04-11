from passenger.views.utils import *
from order.serializers import *
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


@api_view(('POST',))
def PassengerEstimatePriceView(request):
    permission_classes = (IsAuthenticated,)
    if not is_authorized(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    data = request.data
    keys = ['start_POI_lat', 'start_POI_long', 'end_POI_lat', 'end_POI_long']
    for key in keys:
        if key not in data:
            return bad_request_response(f'\'{key}\' is required')

    lat_1 = float(request.data['start_POI_lat'])
    long_1 = float(request.data['start_POI_long'])
    lat_2 = float(request.data['end_POI_lat'])
    long_2 = float(request.data['end_POI_long'])

    payload = {
        'est_price': est_price(lat_1, long_1, lat_2, long_2)
    }
    return payload_response(payload)


@api_view(('POST',))
def PassengerNewOrderView(request):
    # Places an order and record the order into the database
    permission_classes = (IsAuthenticated,)
    if not is_authorized(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if pending_order_exists(passenger_id):
        return bad_request_response('There is already an active order.')

    serializer = PassengerNewOrderSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return payload_response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(('GET',))
def PassengerCurrentOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_authorized(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if not pending_order_exists(passenger_id):
        return bad_request_response('You do not have an active order.')

    order = get_current_order(passenger_id)
    order = model_to_dict(order)
    serializer = PassengerNewOrderSerializer(
        data=order,
        context={'request': request}
    )
    if serializer.is_valid():
        return payload_response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(('GET',))
def PassengerCancelOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_authorized(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if pending_order_exists(passenger_id):
        cancel_current_order(passenger_id)

    return payload_response({})


@api_view(('POST',))
def PassengerUpdateLocationView(request):
    permission_classes = (IsAuthenticated,)
    if not is_authorized(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if not pending_order_exists(passenger_id):
        return bad_request_response('You do not have an active order.')

    data = request.data
    keys = ['passenger_lat', 'passenger_long']
    for key in keys:
        if key not in data:
            return bad_request_response(f'\'{key}\' is required')

    update_location(passenger_id,
                    data['passenger_lat'],
                    data['passenger_long'])
    order = get_current_order(passenger_id)
    order = model_to_dict(order)
    serializer = PassengerNewOrderSerializer(
        data=order,
        context={'request': request}
    )
    if serializer.is_valid():
        return payload_response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(('GET',))
def PassengerListOrdersView(request):
    permission_classes = (IsAuthenticated,)
    if not is_authorized(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 10))

    orders = Order.objects.filter(
        passenger__id=passenger_id
    )
    orders = [model_to_dict(x) for x in orders]
    orders = orders[offset:offset+limit]

    serializer = PassengerNewOrderSerializer(
        data=orders,
        many=True
    )
    if serializer.is_valid():
        return payload_response(serializer.data)
    return Response(serializer.errors, status=400)
