from django.urls import path
from .views import get_orders

urlpatterns = [
    path('delivery/', get_orders, name='get_orders'),
]
