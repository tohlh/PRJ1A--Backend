from django.urls import path
from passenger.auth import *
from passenger.views.info import *
from passenger.views.order import *


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
     # passenger's info
     path('info',
          PassengerInfoView,
          name='passenger_info'),
     # passenger's order
     path('order/new',
          PassengerNewOrderView,
          name='new_order'),
]
