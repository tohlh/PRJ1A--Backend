from message.models import DriverMessage
from rest_framework import serializers
from order.utils import *
from order.models import Order
from message.models import DriverMessage
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


class PathFieldSerializer(serializers.Serializer):
    def to_representation(self, instance):
        before_pickup = instance.before_pickup_path
        if before_pickup == '':
            before_pickup = dict_list_to_base64_json([])
        before_pickup = base64_json_to_dict_list(before_pickup)

        after_pickup = instance.after_pickup_path
        if after_pickup == '':
            after_pickup = dict_list_to_base64_json([])
        after_pickup = base64_json_to_dict_list(after_pickup)

        return {
            'before_pickup_path': before_pickup,
            'after_pickup_path': after_pickup
        }


class PassengerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['username', 'phone']


class DirectionFieldSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return get_direction(
            instance.start_POI_lat,
            instance.start_POI_long,
            instance.end_POI_lat,
            instance.end_POI_long
        )


class DriverOngoingOrderSerializer(serializers.ModelSerializer):
    start = StartPointSerializer(source='*')
    end = EndPointSerializer(source='*')
    points = DirectionFieldSerializer(source='*')
    paths = PathFieldSerializer(source='*')
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
    paths = PathFieldSerializer(source='*')
    passenger = PassengerInfoSerializer()
    price = serializers.DecimalField(source='real_price',
                                     default='0',
                                     max_digits=6,
                                     decimal_places=2)

    class Meta:
        model = Order
        fields = ['start', 'end', 'paths', 'id',
                  'passenger', 'distance', 'price',
                  'status']


class DriverMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverMessage
        fields = ['title', 'description', 'created_at', 'value', 'color']
