from django.db import models

from items.models import OrderedItem
from staff.models import Receiver
from supplier.models import Supplier

class Delivery(models.Model):
    delivery_number = models.AutoField(primary_key = True)
    date = models.CharField(max_length = 100)
    time = models.CharField(max_length = 15)
    receiver = models.ForeignKey(Receiver, on_delete = models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE)
    item = models.OneToOneField(OrderedItem, on_delete = models.CASCADE)
    delivered_quantity = models.IntegerField(default=0)

    #get supplier of the order
    # def get_supplier(self):
    #     return self.items.supplier if self.items else None