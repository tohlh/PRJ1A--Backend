from django.urls import path
from driver.auth import *
from driver.views.info import *
from driver.views.order import *
from driver.views.message import *

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
     path('info/reset',
          DriverResetInfoView,
          name='driver_info_reset'),
     # order
     path('order/queue',
          DriverQueueOrderView,
          name='queue_order'),
     path('order/update-location',
          DriverUpdateLocationView,
          name='update_location'),
     path('order/get',
          DriverGetOrderView,
          name='get_order'),
     path('order/current',
          DriverCurrentOrderView,
          name='current_status'),
     path('order/pickup',
          DriverPickupPassengerView,
          name='pickup_passenger'),
     path('order/cancel',
          DriverCancelOrderView,
          name='cancel_order'),
     path('order/end',
          DriverEndOrderView,
          name='end_order'),
     path('order/list',
          DriverListOrdersView,
          name='list_orders'),
     # driver's message
     path('msg',
          DriverMessageView,
          name='driver_message'),
     path('msg/clear',
          DriverClearMessageView,
          name='clear_message')
]
