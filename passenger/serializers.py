from driver.models import Driver
from rest_framework import serializers
from order.models import Order
from driver.models import Driver
from passenger.views.utils import *


class StartPointSerializer(serializers.Serializer):
    name = serializers.CharField(source='start_POI_name', max_length=150)
    address = serializers.CharField(source='start_POI_address', max_length=150)
    latitude = serializers.FloatField(source='start_POI_lat')
    longitude = serializers.FloatField(source='start_POI_long')


class EndPointSerializer(serializers.Serializer):
    name = serializers.CharField(source='end_POI_name', max_length=150)
    address = serializers.CharField(source='end_POI_address', max_length=150)
    latitude = serializers.FloatField(source='end_POI_lat')
    longitude = serializers.FloatField(source='end_POI_long')


class DriverInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['carplate', 'phone']


class PassengerOrderSerializer(serializers.ModelSerializer):
    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    driver = DriverInfoSerializer()

    class Meta:
        model = Order
        fields = ['start', 'end', 'id', 'driver', 'distance']
