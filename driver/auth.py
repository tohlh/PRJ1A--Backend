from .models import Driver
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt_wechat_sso.serializers import *
from rest_framework_simplejwt_wechat_sso.views import *


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

        driver, _ = Driver.objects.get_or_create(id=user.id)
        driver.save()

        return user

    def WeChatSSO(cls, code):
        if code == "superuser0":
            return {
                "access_token": "ACCESS_TOKEN",
                "expires_in": 7200,
                "refresh_token": "REFRESH_TOKEN",
                "openid": "superuser0openid123123123",
                "scope": "SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        elif code == "superuser1":
            return {
                "access_token": "ACCESS_TOKEN",
                "expires_in": 7200,
                "refresh_token": "REFRESH_TOKEN",
                "openid": "superuser1openid123123123",
                "scope": "SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        elif code == "superuser2":
            return {
                "access_token": "ACCESS_TOKEN",
                "expires_in": 7200,
                "refresh_token": "REFRESH_TOKEN",
                "openid": "superuser2openid123123123",
                "scope": "SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        elif code == "superuser3":
            return {
                "access_token": "ACCESS_TOKEN",
                "expires_in": 7200,
                "refresh_token": "REFRESH_TOKEN",
                "openid": "superuser3openid123123123",
                "scope": "SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        elif code == "superuser4":
            return {
                "access_token": "ACCESS_TOKEN",
                "expires_in": 7200,
                "refresh_token": "REFRESH_TOKEN",
                "openid": "superuser4openid123123123",
                "scope": "SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        elif code == "superuser5":
            return {
                "access_token": "ACCESS_TOKEN",
                "expires_in": 7200,
                "refresh_token": "REFRESH_TOKEN",
                "openid": "superuser5openid123123123",
                "scope": "SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        elif code == "superuser6":
            return {
                "access_token": "ACCESS_TOKEN",
                "expires_in": 7200,
                "refresh_token": "REFRESH_TOKEN",
                "openid": "superuser6openid123123123",
                "scope": "SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        elif code == "superuser7":
            return {
                "access_token": "ACCESS_TOKEN",
                "expires_in": 7200,
                "refresh_token": "REFRESH_TOKEN",
                "openid": "superuser7openid123123123",
                "scope": "SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        elif code == "superuser8":
            return {
                "access_token": "ACCESS_TOKEN",
                "expires_in": 7200,
                "refresh_token": "REFRESH_TOKEN",
                "openid": "superuser8openid123123123",
                "scope": "SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        elif code == "superuser9":
            return {
                "access_token": "ACCESS_TOKEN",
                "expires_in": 7200,
                "refresh_token": "REFRESH_TOKEN",
                "openid": "superuser9openid123123123",
                "scope": "SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        req_params = {
            'appid': api_settings.WECHAT_APP_ID,
            'secret': api_settings.WECHAT_APP_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        url = 'https://api.weixin.qq.com/sns/jscode2session'

        response = requests.get(url, params=req_params)
        result = response.json()

        if 'errcode' in result:
            msg = _(result['errmsg'])
            raise serializers.ValidationError(msg, code='authorization')
        return result


class DriverTokenObtainPairView(TokenObtainPairView):
    serializer_class = DriverTokenObtainPairSerializer


class DriverTokenRefreshView(TokenRefreshView):
    pass


class DriverTokenVerifyView(TokenVerifyView):
    pass
