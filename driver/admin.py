from django.contrib import admin
from .models import Driver


class DriverAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone', 'carplate', 'identification_no']


admin.site.register(Driver, DriverAdmin)
