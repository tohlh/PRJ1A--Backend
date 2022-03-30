from .models import Driver
from django.contrib.auth import get_user_model
from rest_framework_simplejwt_wechat_sso.serializers import (
    TokenObtainPairSerializer
)
from rest_framework_simplejwt_wechat_sso.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


class DriverTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = cls.token_class.for_user(user)
        token["type"] = "driver"
        return token

    def create_or_get_user(cls, openid):
        user, _ = get_user_model().objects.get_or_create(
            username=openid, defaults={'password': openid}
        )
        user.set_password(openid)
        user.save()

        driver, _ = Driver.objects.get_or_create(id=user.id, username=openid)
        driver.save()

        return user


class DriverTokenObtainPairView(TokenObtainPairView):
    serializer_class = DriverTokenObtainPairSerializer


class DriverTokenRefreshView(TokenRefreshView):
    pass


class DriverTokenVerifyView(TokenVerifyView):
    pass
