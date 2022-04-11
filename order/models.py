from django.db import models
from passenger.models import Passenger
from driver.models import Driver


class Order(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.DO_NOTHING)
    driver = models.ForeignKey(Driver, blank=True, null=True, on_delete=models.DO_NOTHING)

    # Only used before the driver picks up the passenger
    passenger_lat = models.FloatField()
    passenger_long = models.FloatField()

    start_POI_name = models.CharField(max_length=150)
    start_POI_address = models.CharField(max_length=150)
    start_POI_lat = models.FloatField()
    start_POI_long = models.FloatField()

    end_POI_name = models.CharField(max_length=150)
    end_POI_address = models.CharField(max_length=150)
    end_POI_lat = models.FloatField()
    end_POI_long = models.FloatField()
    
    # Encode a list of coordinates with Base64
    before_pickup_path = models.TextField()
    after_pickup_path = models.TextField()
    # Distance based on after_pickup_path
    distance = models.DecimalField(default='0', max_digits=6, decimal_places=2)

    est_price = models.DecimalField(max_digits=6, decimal_places=2)
    real_price = models.DecimalField(default='0', max_digits=6, decimal_places=2)

    # Only used before the driver picks up the passenger
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    
    # After the order is fulfilled
    ended_at = models.DateTimeField(blank=True, null=True)
    status = models.PositiveIntegerField()
    """
    status explained
    0, pending (waiting for driver)
    1, driver assigned
    2, picked up by driver
    3, cancelled by passenger
    4, cancelled by driver
    5, done (unpaid)
    6, done (paid)
    """
