from django.urls import path
from .views import get_orders, mark_delivered

urlpatterns = [
    path('delivery/', get_orders, name='get_orders'),
    path('delivery/mark_delivered', mark_delivered, name='mark_delivered')
]
