from django.db import models


class Driver(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    username = models.CharField(max_length=150)
    carplate = models.CharField(max_length=10)
