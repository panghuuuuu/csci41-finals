from django.contrib import admin
from .models import *

# Register your models here.
class AgentAdmin(admin.ModelAdmin):
    list_display = ('agent_number', 'client', 'agent_first_name', 'agent_last_name', 'agent_phone_number')

class SalesAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'agent', 'sales_date',)

admin.site.register(Agent, AgentAdmin)
admin.site.register(Sales, SalesAdmin)