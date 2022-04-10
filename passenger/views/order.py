from passenger.views.utils import *
from passenger.models import Passenger
from passenger.serializers import NewOrderSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


@api_view(('POST',))
def PassengerNewOrderView(request):
    # Places an order and record the order into the database
    permission_classes = (IsAuthenticated,)
    if not is_authorized(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    if pending_order_exists(passenger_id):
        return bad_request_response('There is already an active order.')

    data = JSONParser().parse(request)
    serializer = NewOrderSerializer(
        data=data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return payload_response(serializer.data)
    return Response(serializer.errors, status=400)
