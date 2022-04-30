from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_POI_name', 'end_POI_name',
                    'distance', 'real_price']


admin.site.register(Order, OrderAdmin)
