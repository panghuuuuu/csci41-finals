from django.db import models
from django.core.exceptions import ValidationError
from supplier.models import Supplier
# Create your models here.
class Item(models.Model):

    TIMEPIECES = 'Timepieces'
    DIGITAL_CAMERAS = 'Digital Cameras and Accessories'
    MOBILE_PHONES = 'Mobile Phones'
    SMALL_APPLIANCES = 'Small Appliances'

    ITEM_TYPE_CHOICES = [
        (TIMEPIECES, 'Timepieces'),
        (DIGITAL_CAMERAS, 'Digital Cameras and Accessories'),
        (MOBILE_PHONES, 'Mobile Phones'),
        (SMALL_APPLIANCES, 'Small Appliances') ]

    item_number = models.AutoField(primary_key = True, unique = True)
    item_brand = models.CharField(max_length = 300)
    item_model = models.CharField(max_length = 300)
    item_qty = models.IntegerField()
    item_type = models.CharField(max_length = 300, choices = ITEM_TYPE_CHOICES)
    item_cost = models.DecimalField(max_digits = 10, decimal_places = 3) 
    item_SRP = models.DecimalField(max_digits = 10, decimal_places = 3) 
    item_total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, default='temp_default_value')
    
    def save(self, *args, **kwargs):
        existing_item = Item.objects.filter(item_brand=self.item_brand, supplier=self.supplier, item_model=self.item_model).exclude(item_number=self.item_number).first()
        if existing_item:
            raise ValidationError("An item with the same brand already exists under this supplier.")

        if self.item_total_cost is not None:
            self.item_total_cost = self.item_cost * self.item_qty
        else:
            self.total_cost = 0
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.item_brand} {self.item_model}"


class SoldItem(models.Model):
    item = models.OneToOneField(Item, on_delete = models.CASCADE)
    sold_quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        self.total_sales = self.sold_quantity * self.item_total_cost
    
    def __str__(self):
        return f"SoldItem: {self.item.item_brand} {self.item.item_model}"

class OrderedItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    order = models.ForeignKey('staff.Order', on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    staff_member = models.ForeignKey('staff.Receiver', on_delete=models.CASCADE)
    order_total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    def save(self, *args, **kwargs):
        if self.order_total_cost is not None:
            self.order_total_cost = self.item.item_cost * self.order_quantity
        else:
            self.order_total_cost = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.order_number}: {self.item.item_brand} {self.order_quantity} pcs"

class DeliveredItem(models.Model):
    order = models.ForeignKey('OrderedItem', on_delete=models.CASCADE)

    def __str__(self):
        return f"DeliveredItem: {self.order.item.item_brand}: {self.order.order_quantity} pcs"

class IssuedItem(models.Model):
    item = models.OneToOneField(Item, on_delete = models.CASCADE)
    issued_quantity = models.IntegerField()

    def __str__(self):
        return f"IssuedItem: {self.item.item_brand}: {issued_quantity} pcs"

class ReturnedItem(models.Model):
    item = models.OneToOneField(Item, on_delete = models.CASCADE)
    returned_quantity = models.IntegerField()

    def __str__(self):
        return f"ReturnedItem: {self.item.item_brand}: {returned_quantity} pcs"

class BatchInventory(models.Model):
    batch_inventory = models.ManyToManyField(DeliveredItem)

class ItemType(models.Model):

    TIMEPIECES = 'Timepieces'
    DIGITAL_CAMERAS = 'Digital Cameras and Accessories'
    MOBILE_PHONES = 'Mobile Phones'
    SMALL_APPLIANCES = 'Small Appliances'

    ITEM_TYPE_CHOICES = [
        (TIMEPIECES, 'Timepieces'),
        (DIGITAL_CAMERAS, 'Digital Cameras and Accessories'),
        (MOBILE_PHONES, 'Mobile Phones'),
        (SMALL_APPLIANCES, 'Small Appliances'),]

    item_id = models.IntegerField() #possible values 0-3 not sure
    item_type_name = models.CharField(max_length = 300, choices = ITEM_TYPE_CHOICES)
    discount_rate = models.DecimalField(max_digits = 5, decimal_places = 2)
