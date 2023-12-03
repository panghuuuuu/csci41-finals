from django.urls import path
from .views import get_orders, mark_delivered, get_supplier_inventory

urlpatterns = [
    path('delivery/', get_orders, name='get_orders'),
    path('delivery/mark_delivered', mark_delivered, name='mark_delivered'),
    path('get_supplier_inventory/', get_supplier_inventory, name='get_supplier_inventory')
]
