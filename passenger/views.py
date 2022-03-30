import jwt
from prj1a.settings import SIMPLE_JWT
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(('GET',))
def PasasengerProtectedView(request):
    permission_classes = (IsAuthenticated,)
    encoded_token = request.META.get('HTTP_AUTHORIZATION')[7:]
    decoded_token = jwt.decode(
        encoded_token,
        SIMPLE_JWT['SIGNING_KEY'],
        algorithms=[SIMPLE_JWT['ALGORITHM']])

    if decoded_token['type'] == 'passenger':
        return Response({
            "response": "you are authorized to access this API"
        })
    else:
        return Response({
            "response": "you are not authorized to access this API"
        }, 401)
