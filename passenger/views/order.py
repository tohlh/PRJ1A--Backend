from passenger.views.utils import *
from passenger.models import Passenger
from passenger.serializers import NewOrderSerializer
from rest_framework.parsers import JSONParser
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

    serializer = NewOrderSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return payload_response(serializer.data)
    return Response(serializer.errors, status=400)
