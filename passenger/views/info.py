from passenger.models import Passenger
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from passenger.views.utils import *


@api_view(('GET', 'POST'))
def PassengerInfoView(request):
    permission_classes = (IsAuthenticated,)
    if not is_passenger(request):
        return unauthorized_response()
    passenger_id = get_passenger_id(request)

    def passenger_info_response(passenger_id):
        passenger_object = Passenger.objects.get(id=passenger_id)
        payload = {
            'username': passenger_object.username,
            'phone': passenger_object.phone,
            'age': passenger_object.age,
            'identification_no': passenger_object.identification_no
        }
        return payload_response(payload)

    if request.method == 'GET':
        return passenger_info_response(passenger_id)
    elif request.method == 'POST':
        data = request.data
        fields = ['username', 'phone',
                  'age', 'identification_no']

        for field in fields:
            if field not in data:
                return bad_request_response({
                    'ErrMsg': f'{field} is required'
                })

        Passenger.objects.filter(id=passenger_id).update(
            username=data['username'],
            phone=data['phone'],
            age=data['age'],
            identification_no=data['identification_no']
        )
        return passenger_info_response(passenger_id)

    return internal_error_response()
