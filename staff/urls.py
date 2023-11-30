from django.urls import path
from .views import order_item, get_items, submit_order, login_view, logout_view, fetch_ordered_items

urlpatterns = [
    path('order/', get_items, name='get_items'),
    path('order/order_item/', order_item, name='order_item'),
    path('order/receipt', submit_order, name='submit_order'),
    path('login/', login_view, name='login_view'),  
    path('logout/', logout_view, name='logout_view'),
    path('fetch_ordered_items/', fetch_ordered_items, name='fetch_ordered_items'),
]
