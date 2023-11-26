from django.urls import path
from .views import order_item, get_items, submit_order, select_staff

urlpatterns = [
    path('order/', get_items, name='get_items'),
    path('order/order_item/', order_item, name='order_item'),
    path('order/', submit_order, name='submit_order'),
]
