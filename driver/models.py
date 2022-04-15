from django.db import models


class Driver(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    username = models.CharField(max_length=150)
    age = models.PositiveIntegerField(null=True, blank=True)
    identification_no = models.CharField(max_length=20)
    carplate = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    last_online = models.DateTimeField(auto_now=True)
