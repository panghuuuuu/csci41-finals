from django.db import models

from items.models import DeliveredItem
from staff.models import Receiver
from supplier.models import Supplier, Delivery

class Delivery(models.Model):
    delivery_number = models.AutoField(primary_key=True, unique=True)
    order = models.ForeignKey("staff.Order", on_delete=models.CASCADE, null=True, blank=True, related_name='delivered_orders')
    delivered_items = models.ManyToManyField("items.DeliveredItem", related_name='delivered_items')
    delivery_date = models.DateField(auto_now_add=True)
    delivery_time = models.TimeField(auto_now_add=True)
            
    def __str__(self):
        return f"{self.delivery_number} {self.delivery_date}"