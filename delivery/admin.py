from django.contrib import admin
from items.models import Item
from .models import *

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_number', 'delivery_date')

admin.site.register(Delivery, DeliveryAdmin)