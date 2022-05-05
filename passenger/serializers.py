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


class PointsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if instance.status <= 2:
            ret, _ = get_direction(
                instance.start_POI_lat,
                instance.start_POI_long,
                instance.end_POI_lat,
                instance.end_POI_long
            )
            return ret

        path_list = instance.after_pickup_path
        if path_list == '':
            path_list = dict_list_to_base64_json([])
        path_list = base64_json_to_dict_list(path_list)
        return path_list


class DistanceSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if instance.status <= 2:
            _, dist = get_direction(
                instance.start_POI_lat,
                instance.start_POI_long,
                instance.end_POI_lat,
                instance.end_POI_long
            )
            return dist
        return instance.distance


class PriceSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if instance.status <= 2:
            return instance.est_price
        elif instance.status <= 4:
            return 0
        elif instance.status <= 6:
            return instance.real_price


class TimeSerializer(serializers.Serializer):
    create = serializers.DateTimeField(source='created_at')
    end = serializers.DateTimeField(source='ended_at')


class PassengerOrderInfoSerializer(serializers.ModelSerializer):
    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    price = serializers.DecimalField(source='est_price',
                                     max_digits=6,
                                     decimal_places=2)
    distance = DistanceSerializer(source='*')
    points = PointsSerializer(source='*')
    driver = DriverInfoSerializer()

    class Meta:
        model = Order
        fields = ['start', 'end', 'id',
                  'points', 'distance', 'price',
                  'status', 'driver']


class PassengerOrderListSerializer(serializers.ModelSerializer):
    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    price = serializers.DecimalField(source='real_price',
                                     max_digits=6,
                                     decimal_places=2)
    time = TimeSerializer(source='*')

    class Meta:
        model = Order
        fields = ['start', 'end', 'id',
                  'distance', 'price',
                  'status', 'time']


class PassengerOrderDetailSerializer(serializers.ModelSerializer):
    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    points = PointsSerializer(source='*')
    driver = DriverInfoSerializer()

    class Meta:
        model = Order
        fields = ['start', 'end', 'id', 'driver'
                  'price', 'distance', 'points'
                  'status']
