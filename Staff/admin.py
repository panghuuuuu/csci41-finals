from django.contrib import admin
from .models import Staff, Receiver, Issuer

class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_number', 'staff_first_name', 'staff_last_name', 'staff_phone_number', 'staff_type')
    search_fields = ('staff_first_name', 'staff_last_name', 'staff_type')

class ReceiverAdmin(admin.ModelAdmin):
    list_display = ('receiver_number', 'staff')
    search_fields = ('staff__staff_first_name', 'staff__staff_last_name')

class IssuerAdmin(admin.ModelAdmin):
    list_display = ('issuer_number', 'staff')
    search_fields = ('staff__staff_first_name', 'staff__staff_last_name')

admin.site.register(Staff, StaffAdmin)
admin.site.register(Receiver, ReceiverAdmin)
admin.site.register(Issuer, IssuerAdmin)