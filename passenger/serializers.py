from rest_framework import serializers
from order.models import Order
from passenger.models import Passenger
from passenger.views.utils import *
from django.utils import timezone


class PassengerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'driver', 'passenger',
                  'passenger_lat', 'passenger_long',
                  'start_POI_name', 'start_POI_address', 'start_POI_lat',
                  'start_POI_long', 'end_POI_name', 'end_POI_address',
                  'end_POI_lat', 'end_POI_long', 'est_price', 'status',
                  'updated_at', 'created_at']
