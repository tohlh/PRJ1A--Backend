from rest_framework import serializers
from order.models import Order
from passenger.models import Passenger
from driver.views.utils import *


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


class PathsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['before_pickup_path', 'after_pickup_path']


class PassengerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['phone']


class DriverOrderSerializer(serializers.ModelSerializer):
    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    paths = PathsSerializer(source='*')
    passenger = PassengerInfoSerializer()

    class Meta:
        model = Order
        fields = ['start', 'end', 'paths', 'id', 'passenger', 'distance']
