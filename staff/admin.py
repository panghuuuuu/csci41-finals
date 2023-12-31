from django.contrib import admin
from .models import *

class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_number', 'staff_first_name', 'staff_last_name', 'staff_phone_number', 'staff_type')
    search_fields = ('staff_first_name', 'staff_last_name', 'staff_type')

class ReceiverAdmin(admin.ModelAdmin):
    list_display = ('receiver_number', 'staff')
    search_fields = ('staff__staff_first_name', 'staff__staff_last_name')

class IssuerAdmin(admin.ModelAdmin):
    list_display = ('issuer_number', 'staff')
    search_fields = ('staff__staff_first_name', 'staff__staff_last_name')

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'receiver')

class IssuanceAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'issuer')


class TransferAdmin(admin.ModelAdmin):
    list_display = ('transfer_number', 'isComplete')

class ReturnAdmin(admin.ModelAdmin):
    list_display = ('batch', 'return_date')

admin.site.register(Staff, StaffAdmin)
admin.site.register(Receiver, ReceiverAdmin)
admin.site.register(Issuer, IssuerAdmin)
admin.site.register(Order, OrdersAdmin)
admin.site.register(Issuance, IssuanceAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(Return, ReturnAdmin)