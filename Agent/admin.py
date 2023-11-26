from django.contrib import admin
from .models import *

# Register your models here.
class AgentAdmin(admin.ModelAdmin):
    list_display = ('agent_number', 'agent_first_name', 'agent_last_name', 'agent_phone_number')

admin.site.register(Agent, AgentAdmin)