from .views.info import PassengerInfoView
from django.urls import path
from passenger.auth import (
    PassengerTokenObtainPairView,
    PassengerTokenRefreshView,
    PassengerTokenVerifyView,
)

urlpatterns = [
     # passenger's tokens
     path('token',
          PassengerTokenObtainPairView.as_view(),
          name='passenger_token_obtain_pair'),
     path('token/refresh',
          PassengerTokenRefreshView.as_view(),
          name='passenger_token_refresh'),
     path('token/verify',
          PassengerTokenVerifyView.as_view(),
          name='passenger_token_verify'),
     # driver's info
     path('info',
          PassengerInfoView,
          name='passenger_info'),
]
