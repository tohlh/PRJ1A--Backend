from driver.views.utils import *
from driver.serializers import *
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


@api_view(('POST',))
def DriverQueueOrderView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    return payload_response({})


@api_view(('POST',))
def DriverUpdateLocation(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)
    
    latitude = driver

    return payload_response({})