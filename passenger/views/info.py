from passenger.models import Passenger
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from passenger.views.utils import (
    get_passenger_id,
    is_authorized,
    payload_response,
    unauthorized_response,
    internal_error_response
)


@api_view(('GET', 'POST'))
def PassengerInfoView(request):
    permission_classes = (IsAuthenticated,)
    if not is_authorized:
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    def passenger_info_response(passenger_id):
        passenger_object = Passenger.objects.get(id=passenger_id)
        payload = {
            'username': passenger_object.username,
        }
        return payload_response(payload)

    if request.method == 'GET':
        return passenger_info_response(passenger_id)
    elif request.method == 'POST':
        Passenger.objects.filter(id=passenger_id).update(
            username=request.data['username'],
        )
        return passenger_info_response(passenger_id)

    return internal_error_response()
