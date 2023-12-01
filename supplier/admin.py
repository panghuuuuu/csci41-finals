from django.contrib import admin
from .models import Supplier, Delivery

# Register your models here.
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_name', 'supplier_phone_number')

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_number', 'delivery_date')

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Delivery, DeliveryAdmin)