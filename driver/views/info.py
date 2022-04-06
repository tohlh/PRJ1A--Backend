from driver.models import Driver
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from driver.views.utils import (
    get_driver_id,
    is_authorized,
    payload_response,
    unauthorized_response,
    internal_error_response
)


@api_view(('GET', 'POST'))
def DriverInfoView(request):
    permission_classes = (IsAuthenticated,)
    if not is_authorized(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    def driver_info_response(driver_id):
        driver_object = Driver.objects.get(id=driver_id)
        payload = {
            'username': driver_object.username,
            'carplate': driver_object.carplate,
        }
        return payload_response(payload)

    if request.method == 'GET':
        return driver_info_response(driver_id)
    elif request.method == 'POST':
        Driver.objects.filter(id=driver_id).update(
            username=request.data['username'],
            carplate=request.data['carplate']
        )
        return driver_info_response(driver_id)

    return internal_error_response()
