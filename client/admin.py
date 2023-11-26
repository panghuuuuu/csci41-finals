from django.contrib import admin
from .models import *

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_office_address', 'client_email_address')

admin.site.register(Client, ClientAdmin)