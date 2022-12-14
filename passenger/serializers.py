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


class PassengerOrderInfoSerializer(serializers.ModelSerializer):
    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    price = PriceSerializer(source='*')
    distance = DistanceSerializer(source='*')
    points = PointsSerializer(source='*')
    driver = DriverInfoSerializer()

    class Meta:
        model = Order
        fields = ['start', 'end', 'id',
                  'points', 'distance', 'price',
                  'status', 'driver']


class PassengerOrderListSerializer(serializers.ModelSerializer):
    class TimeSerializer(serializers.Serializer):
        create = serializers.DateTimeField(source='created_at')

    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    price = PriceSerializer(source='*')
    time = TimeSerializer(source='*')

    class Meta:
        model = Order
        fields = ['start', 'end', 'id',
                  'distance', 'price',
                  'status', 'time']


class PassengerOrderDetailSerializer(serializers.ModelSerializer):
    class TimeSerializer(serializers.Serializer):
        create = serializers.DateTimeField(source='created_at')
        accept = serializers.DateTimeField(source='accepted_at')
        start = serializers.DateTimeField(source='started_at')
        end = serializers.DateTimeField(source='ended_at')
        paid = serializers.DateTimeField(source='paid_at')
        cancel = serializers.DateTimeField(source='canceled_at')

    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    points = PointsSerializer(source='*')
    price = PriceSerializer(source='*')
    time = TimeSerializer(source='*')
    driver = DriverInfoSerializer()

    class Meta:
        model = Order
        fields = ['start', 'end', 'id', 'driver',
                  'price', 'distance', 'points',
                  'status', 'time']
