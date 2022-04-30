from rest_framework import serializers
from order.utils import *
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
        fields = ['username', 'phone']


class RouteFieldSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return get_direction(
            instance.start_POI_lat,
            instance.start_POI_long,
            instance.end_POI_lat,
            instance.end_POI_long
        )


class DriverOngoingOrderSerializer(serializers.ModelSerializer):
    points = RouteFieldSerializer(source='*')
    paths = PathsSerializer(source='*')
    passenger = PassengerInfoSerializer()
    price = serializers.DecimalField(source='est_price',
                                     default='0',
                                     max_digits=6,
                                     decimal_places=2)

    class Meta:
        model = Order
        fields = ['points', 'paths', 'id',
                  'passenger', 'distance', 'price',
                  'status']


class DriverCompletedOrderSerializer(serializers.ModelSerializer):
    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    paths = PathsSerializer(source='*')
    passenger = PassengerInfoSerializer()
    price = serializers.DecimalField(source='real_price',
                                     default='0',
                                     max_digits=6,
                                     decimal_places=2)

    class Meta:
        model = Order
        fields = ['start', 'end', 'paths', 'id',
                  'passenger', 'distance', 'real_price',
                  'status']
