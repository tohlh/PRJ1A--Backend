from rest_framework import serializers
from order.models import Order
from passenger.models import Passenger
from passenger.views.utils import *
from django.utils import timezone


class PassengerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['driver', 'passenger_lat', 'passenger_long',
                  'start_POI_name', 'start_POI_address', 'start_POI_lat',
                  'start_POI_long', 'end_POI_name', 'end_POI_address',
                  'end_POI_lat', 'end_POI_long', 'est_price', 'status']


class PassengerNewOrderSerializer(serializers.Serializer):
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
        passenger_id = self.context.get('passenger_id')
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
