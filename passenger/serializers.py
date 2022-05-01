from rest_framework import serializers
from order.models import Order
from order.utils import *
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
        fields = ['username', 'carplate', 'phone']


class DirectionFieldSerializer(serializers.Serializer):
    def to_representation(self, instance):
        ret, _ = get_direction(
            instance.start_POI_lat,
            instance.start_POI_long,
            instance.end_POI_lat,
            instance.end_POI_long
        )
        return ret


class PathFieldSerializer(serializers.Serializer):
    def to_representation(self, instance):
        path_list = instance.before_pickup_path
        if path_list == '':
            path_list = dict_list_to_base64_json([])
        path_list = base64_json_to_dict_list(path_list)
        return path_list


class PassengerOngoingOrderSerializer(serializers.ModelSerializer):
    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    driver = DriverInfoSerializer()
    price = serializers.DecimalField(source='est_price',
                                     max_digits=6,
                                     decimal_places=2)
    points = DirectionFieldSerializer(source='*')

    class Meta:
        model = Order
        fields = ['start', 'end', 'id',
                  'driver', 'distance', 'price',
                  'status', 'points']


class PassengerCompletedOrderSerializer(serializers.ModelSerializer):
    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    driver = DriverInfoSerializer()
    price = serializers.DecimalField(source='real_price',
                                     max_digits=6,
                                     decimal_places=2)
    points = PathFieldSerializer(source='*')

    class Meta:
        model = Order
        fields = ['start', 'end', 'id',
                  'driver', 'distance', 'price',
                  'status', 'points']
