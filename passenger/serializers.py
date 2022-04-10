from rest_framework import serializers
from order.models import Order
from passenger.views.utils import *
from passenger.models import Passenger


class NewOrderSerializer(serializers.Serializer):
    passenger_lat = serializers.FloatField(required=True)
    passenger_long = serializers.FloatField(required=True)

    start_POI_name = serializers.CharField(required=True, max_length=150)
    start_POI_address = serializers.CharField(required=True, max_length=150)
    start_POI_lat = serializers.FloatField(required=True)
    start_POI_long = serializers.FloatField(required=True)

    end_POI_name = serializers.CharField(required=True, max_length=150)
    end_POI_address = serializers.CharField(required=True, max_length=150)
    end_POI_lat = serializers.FloatField(required=True)
    end_POI_long = serializers.FloatField(required=True)

    def create(self, validated_data):
        request = self.context.get('request')
        passenger_id = get_passenger_id(request)
        validated_data['passenger'] = Passenger.objects.get(id=passenger_id)
        validated_data['status'] = 1
        return Order.objects.create(**validated_data)
