from django.urls import path
from .views import *

urlpatterns = [
    path('sales', get_agents, name='get_agents'),
    path('sales/sold_items', input_sales, name='input_sales'),
    path('sales/submit_sales', submit_sales, name='submit_sales'),


]
