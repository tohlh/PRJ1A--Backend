from django.urls import path
from driver.auth import *
from driver.views.info import *
from driver.views.order import *

urlpatterns = [
     # driver's tokens
     path('token',
          DriverTokenObtainPairView.as_view(),
          name='driver_token_obtain_pair'),
     path('token/refresh',
          DriverTokenRefreshView.as_view(),
          name='driver_token_refresh'),
     path('token/verify',
          DriverTokenVerifyView.as_view(),
          name='driver_token_verify'),
     # driver's info
     path('info',
          DriverInfoView,
          name='driver_info'),
     # order
     path('order/queue',
          DriverQueueOrderView,
          name='queue_order'),
]
