from .views import PasasengerProtectedView

from django.urls import path

from passenger.auth import (
    PassengerTokenObtainPairView,
    PassengerTokenRefreshView,
    PassengerTokenVerifyView,
)

urlpatterns = [
     path('token',
          PassengerTokenObtainPairView.as_view(),
          name='passenger_token_obtain_pair'),
     path('token/refresh',
          PassengerTokenRefreshView.as_view(),
          name='passenger_token_refresh'),
     path('token/verify',
          PassengerTokenVerifyView.as_view(),
          name='passenger_token_verify'),
     path('protected', PasasengerProtectedView),
]
