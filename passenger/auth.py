from .models import Passenger
from django.contrib.auth import get_user_model
from rest_framework_simplejwt_wechat_sso.serializers import (
    TokenObtainPairSerializer
)
from rest_framework_simplejwt_wechat_sso.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


class PassengerTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = cls.token_class.for_user(user)
        token["type"] = "passenger"
        return token

    def create_or_get_user(cls, openid):
        user, _ = get_user_model().objects.get_or_create(
            username=openid,
            defaults={'password': openid}
        )
        user.set_password(openid)
        user.save()

        passenger, _ = Passenger.objects.get_or_create(id=user.id)
        passenger.save()

        return user


class PassengerTokenObtainPairView(TokenObtainPairView):
    serializer_class = PassengerTokenObtainPairSerializer


class PassengerTokenRefreshView(TokenRefreshView):
    pass


class PassengerTokenVerifyView(TokenVerifyView):
    pass
