from django.urls import path
from .views import * delivery_status

urlpatterns = [
    path('order/', get_items, name='get_items'),
    path('order/order_item/', order_item, name='order_item'),
    path('order/receipt', submit_order, name='submit_order'),
    path('issuance/', get_inventory_and_issued_items, name='get_inventory_and_issued_items'),
    path('issuance/submit_issuance', submit_issuance, name='submit_issuance'),
    path('issuance/issue_item/', issue_item, name='issue_item'),
    path('transfer/', fetch_batch_items, name='fetch_batch_items'),
    path('transfer/transfer_items/', transfer_items, name='transfer_items'),
    path('transfer/complete_transfer', complete_transfer, name='complete_transfer'),
    path('login/', login_view, name='login_view'),  
    path('logout/', logout_view, name='logout_view'),
    path('fetch_ordered_items/', fetch_ordered_items, name='fetch_ordered_items'),
    path('order/delivery_status/', delivery_status, name='delivery_status')
]