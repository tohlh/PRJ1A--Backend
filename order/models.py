from django.db import models
from passenger.models import Passenger
from driver.models import Driver


class Order(models.Model):
    """
    CASCADE means delete this Order when the associated driver or passenger is deleted
    """
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    from_lat = models.FloatField()
    from_long = models.FloatField()
    to_lat = models.FloatField()
    to_long = models.FloatField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.PositiveIntegerField()
    """
    status explained
    0, pending (waiting for driver)
    1, picked up by driver
    2, done
    """
