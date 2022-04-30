from django.db import models
from driver.models import Driver


class DriverMessage(models.Model):
    driver = models.ForeignKey(Driver,
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    value = models.CharField(max_length=150)
    color = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
