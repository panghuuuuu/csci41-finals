from django.db import models

from staff.models import Receiver
from supplier.models import Supplier

class DeliveryReceipt(models.Model):
    delivery_number = models.AutoField(primary_key = True)
    date = models.CharField(max_length = 100)
    time = models.CharField(max_length = 15)
    receiver = models.ForeignKey(Receiver, on_delete = models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE)
    