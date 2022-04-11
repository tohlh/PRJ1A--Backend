from rest_framework import serializers
from order.models import Order
from passenger.views.utils import *
from passenger.models import Passenger
from django.utils import timezone


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

    est_price = serializers.DecimalField(read_only=True,
                                         max_digits=6,
                                         decimal_places=2)

    def create(self, validated_data):
        request = self.context.get('request')
        passenger_id = get_passenger_id(request)
        validated_data['passenger'] = Passenger.objects.get(id=passenger_id)
        validated_data['status'] = 1
        validated_data['est_price'] = est_price(
            validated_data['start_POI_lat'],
            validated_data['start_POI_long'],
            validated_data['end_POI_lat'],
            validated_data['end_POI_long']
        )
        validated_data['updated_at'] = timezone.now()
        return Order.objects.create(**validated_data)


class CurrentOrderSerializer(serializers.Serializer):
    driver = serializers.RelatedField(read_only=True)
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

    est_price = serializers.DecimalField(read_only=True,
                                         max_digits=6,
                                         decimal_places=2)


class ListOrderSerializer(serializers.Serializer):
    driver = serializers.RelatedField(read_only=True)
    passenger_lat = serializers.FloatField(read_only=True)
    passenger_long = serializers.FloatField(read_only=True)

    start_POI_name = serializers.CharField(read_only=True, max_length=150)
    start_POI_address = serializers.CharField(read_only=True, max_length=150)
    start_POI_lat = serializers.FloatField(read_only=True)
    start_POI_long = serializers.FloatField(read_only=True)

    end_POI_name = serializers.CharField(read_only=True, max_length=150)
    end_POI_address = serializers.CharField(read_only=True, max_length=150)
    end_POI_lat = serializers.FloatField(read_only=True)
    end_POI_long = serializers.FloatField(read_only=True)
