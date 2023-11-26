from django.db import models
from items.models import Item, OrderedItem
from supplier.models import Supplier
# Create your models here.
class Staff(models.Model):

    REGULAR = 'Regular'
    ISSUER = 'Issuer'
    RECEIVER = 'Receiver'

    STAFF_TYPE_CHOICES = [
        (REGULAR, 'Regular'),
        (ISSUER, 'Issuer'),
        (RECEIVER, 'Receiver'),
    ]

    staff_number = models.AutoField(primary_key = True, unique = True)
    staff_first_name = models.CharField(max_length = 300)
    staff_last_name = models.CharField(max_length = 300)
    staff_phone_number = models.IntegerField()
    staff_type = models.CharField(max_length = 300, choices = STAFF_TYPE_CHOICES)

class Receiver(models.Model):
    staff = models.OneToOneField(Staff, on_delete = models.CASCADE)
    receiver_number = models.AutoField(primary_key = True)

    def __str__(self):
        return f"Receiver: {self.staff.staff_first_name} {self.staff.staff_last_name}"

class Issuer(models.Model):
    staff = models.OneToOneField(Staff, on_delete = models.CASCADE)
    issuer_number = models.AutoField(primary_key = True)

    def __str__(self):
        return f"Issuer: {self.staff.staff_first_name} {self.staff.staff_last_name}"

class Order(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    ordered_items = models.ManyToManyField(OrderedItem)    
    order_date = models.DateField(auto_now_add=True)