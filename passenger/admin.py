from django.contrib import admin
from .models import Passenger


class PassengerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'phone', 'identification_no']


admin.site.register(Passenger, PassengerAdmin)
