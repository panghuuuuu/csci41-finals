from django.contrib import admin
from items.models import Item
from .models import *

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'supplier')

class ItemInline(admin.TabularInline):
    model = Item

class deliveryAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]

admin.site.register(Delivery, DeliveryAdmin)