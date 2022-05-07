from driver.models import Driver
from driver.serializers import DriverMessageSerializer
from message.models import DriverMessage
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from driver.views.utils import *


@api_view(('GET', 'POST'))
def DriverMessageView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    if driver_unregistered(driver_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    if request.method == 'GET':
        messages = DriverMessage.objects.filter(
            driver__id=driver_id
        ).order_by('-created_at')
        serializer = DriverMessageSerializer(
            messages,
            many=True
        )
        return payload_response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        DriverMessage.objects.create(
            driver=Driver.objects.get(id=driver_id),
            title=data['title'],
            description=data['description'],
            value=data['value'],
            color=data['color']
        )
    return payload_response({})

@api_view(('POST',))
def DriverClearMessageView(request):
    permission_classes = (IsAuthenticated,)
    if not is_driver(request):
        return unauthorized_response()
    driver_id = get_driver_id(request)

    if driver_unregistered(driver_id):
        return unregistered_response({
            'errMsg': '请填写个人资料。'
        })

    DriverMessage.objects.filter(
        driver=Driver.objects.get(id=driver_id)
    ).delete()

    return payload_response({})
