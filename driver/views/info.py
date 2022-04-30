from driver.models import Driver
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from driver.views.utils import *


@api_view(('GET', 'POST'))
def DriverInfoView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    def driver_info_response(driver_id):
        driver_object = Driver.objects.get(id=driver_id)
        payload = {
            'username': driver_object.username,
            'carplate': driver_object.carplate,
            'phone': driver_object.phone,
            'age': driver_object.age,
            'identification_no': driver_object.identification_no
        }
        return payload_response(payload)

    if request.method == 'GET':
        return driver_info_response(driver_id)
    elif request.method == 'POST':
        data = request.data
        fields = ['username', 'carplate', 'phone',
                  'age', 'identification_no']

        for field in fields:
            if field not in data:
                return bad_request_response({
                    'errMsg': f'{field} is required'
                })

        Driver.objects.filter(id=driver_id).update(
            username=data['username'],
            carplate=data['carplate'],
            phone=data['phone'],
            age=data['age'],
            identification_no=data['identification_no']
        )
        return driver_info_response(driver_id)

    return internal_error_response()


@api_view(('POST',))
def DriverResetInfoView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    Driver.objects.filter(
        id=driver_id
    ).update(
            username='',
            phone='',
            carplate='',
            age=None,
            identification_no=''
        )
    return payload_response({})
