from django.db import models
from passenger.models import Passenger
from driver.models import Driver


class StartPOI(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()


class EndPOI(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()


class BeforePathPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class AfterPathPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    """
    CASCADE means delete this Order when the associated driver or passenger is deleted
    """
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    # Only used before the driver picks up the passenger
    passenger_lat = models.FloatField()
    passenger_long = models.FloatField()

    starting_point = models.ForeignKey(StartPOI, on_delete=models.PROTECT)
    ending_point = models.ForeignKey(EndPOI, on_delete=models.PROTECT)
    
    # Started recording when the driver accepts the order
    before_pickup_path = models.ManyToManyField(BeforePathPoint)
    after_pickup_path = models.ManyToManyField(AfterPathPoint)
    # Distance based on after_pickup_path
    distance = models.DecimalField(max_digits=6, decimal_places=2)

    est_price = models.DecimalField(max_digits=6, decimal_places=2)
    real_price = models.DecimalField(max_digits=6, decimal_places=2)

    # Only used before the driver picks up the passenger
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # After the order is fulfilled
    ended_at = models.DateTimeField()
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
