from .views import DriverProtectedView
from django.urls import path

from driver.auth import (
    DriverTokenObtainPairView,
    DriverTokenRefreshView,
    DriverTokenVerifyView,
)

urlpatterns = [
     path('token',
          DriverTokenObtainPairView.as_view(),
          name='driver_token_obtain_pair'),
     path('token/refresh',
          DriverTokenRefreshView.as_view(),
          name='driver_token_refresh'),
     path('token/verify',
          DriverTokenVerifyView.as_view(),
          name='driver_token_verify'),
     path('protected', DriverProtectedView),
]
