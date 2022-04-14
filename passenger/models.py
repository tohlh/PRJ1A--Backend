from django.db import models


class Passenger(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    username = models.CharField(max_length=150)
    phone = models.CharField(max_length=11)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
