from django.db import models
from django.core.exceptions import ValidationError
from supplier.models import Supplier, Delivery
from staff.models import Issuer, Receiver, BatchInventory, Issuance, Order
from client.models import Client
# Create your models here.

class SupplierItem(models.Model):
    TIMEPIECES = 'Timepieces'
    DIGITAL_CAMERAS = 'Digital Cameras and Accessories'
    MOBILE_PHONES = 'Mobile Phones'
    SMALL_APPLIANCES = 'Small Appliances'

    ITEM_TYPE_CHOICES = [
        (TIMEPIECES, 'Timepieces'),
        (DIGITAL_CAMERAS, 'Digital Cameras and Accessories'),
        (MOBILE_PHONES, 'Mobile Phones'),
        (SMALL_APPLIANCES, 'Small Appliances'),
    ]
    supplier_item_number = models.AutoField(primary_key=True, unique=True)
    supplier_item_brand = models.CharField(max_length=300)
    supplier_item_model = models.CharField(max_length=300)
    supplier_item_qty = models.IntegerField()
    supplier_item_type = models.CharField(max_length=300, choices=ITEM_TYPE_CHOICES)
    supplier_item_cost = models.DecimalField(max_digits=10, decimal_places=3)
    supplier_item_total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    supplier =  models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False, blank=False)

    def save(self, *args, **kwargs):
        existing_item = SupplierItem.objects.filter(supplier_item_brand=self.supplier_item_brand, supplier=self.supplier, supplier_item_model=self.supplier_item_model).exclude(supplier_item_number=self.supplier_item_number).first()
        if existing_item:
            raise ValidationError("An item with the same brand and model already exists under this supplier.")

        if self.supplier_item_total_cost is not None:
            self.supplier_item_total_cost = self.supplier_item_cost * self.supplier_item_qty
        else:
            self.supplier_total_cost = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.supplier_item_brand} {self.supplier_item_model}"

class ItemType(models.Model):
    TIMEPIECES = 'Timepieces'
    DIGITAL_CAMERAS = 'Digital Cameras and Accessories'
    MOBILE_PHONES = 'Mobile Phones'
    SMALL_APPLIANCES = 'Small Appliances'

    ITEM_TYPE_CHOICES = [
        (TIMEPIECES, 'Timepieces'),
        (DIGITAL_CAMERAS, 'Digital Cameras and Accessories'),
        (MOBILE_PHONES, 'Mobile Phones'),
        (SMALL_APPLIANCES, 'Small Appliances'),
    ]

    item_type = models.CharField(max_length=300, choices=ITEM_TYPE_CHOICES)
    item_discount = models.DecimalField(max_digits=5, decimal_places=4, default=0.0)
    item_client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.item_supplier} - {self.item_type} ({self.item_discount * 100}%)"

class Item(models.Model):
    TIMEPIECES = 'Timepieces'
    DIGITAL_CAMERAS = 'Digital Cameras and Accessories'
    MOBILE_PHONES = 'Mobile Phones'
    SMALL_APPLIANCES = 'Small Appliances'

    ITEM_TYPE_CHOICES = [
        (TIMEPIECES, 'Timepieces'),
        (DIGITAL_CAMERAS, 'Digital Cameras and Accessories'),
        (MOBILE_PHONES, 'Mobile Phones'),
        (SMALL_APPLIANCES, 'Small Appliances'),
    ]

    item_number = models.AutoField(primary_key=True, unique=True)
    item_brand = models.CharField(max_length=300)
    item_model = models.CharField(max_length=300)
    item_qty = models.IntegerField()
    item_cost = models.DecimalField(max_digits=10, decimal_places=3)
    item_total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    item_type = models.CharField(max_length=300, choices=ITEM_TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.item_brand} {self.item_model} : Quantity: {self.item_qty}"


class OrderedItem(models.Model):
    item = models.ForeignKey('SupplierItem', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    order_total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    
    def save(self, *args, **kwargs):
        if self.order_total_cost is not None:
            self.order_total_cost = self.item.supplier_item_cost * self.order_quantity
        else:
            self.order_total_cost = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.order_number}: {self.item.supplier_item_brand} {self.order_quantity} pcs"

class DeliveredItem(models.Model):
    ordered_item = models.ForeignKey('OrderedItem', on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='delivered_items')

    def __str__(self):
        return f"DeliveredItem: {self.order.item.item_brand}: {self.order.order_quantity} pcs"

class IssuedItem(models.Model):
    TIMEPIECES = 'Timepieces'
    DIGITAL_CAMERAS = 'Digital Cameras and Accessories'
    MOBILE_PHONES = 'Mobile Phones'
    SMALL_APPLIANCES = 'Small Appliances'

    ITEM_TYPE_CHOICES = [
        (TIMEPIECES, 'Timepieces'),
        (DIGITAL_CAMERAS, 'Digital Cameras and Accessories'),
        (MOBILE_PHONES, 'Mobile Phones'),
        (SMALL_APPLIANCES, 'Small Appliances'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    issued_quantity = models.IntegerField()
    item_discount = models.DecimalField(max_digits=10, decimal_places=3)
    issued_SRP = models.DecimalField(max_digits=10, decimal_places=3)
    batch_number = models.ForeignKey(BatchInventory, on_delete=models.CASCADE, related_name='issued_items')
    item_type = models.CharField(max_length=300, choices=ITEM_TYPE_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"IssuedItem: {self.item.item_brand}: {self.issued_quantity} pcs"

class SoldItem(models.Model):
    item = models.OneToOneField(Item, on_delete = models.CASCADE)
    sold_quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        self.total_sales = self.sold_quantity * self.item_total_cost
    
    def __str__(self):
        return f"SoldItem: {self.item.item_brand} {self.item.item_model}"

class ReturnedItem(models.Model):
    item = models.OneToOneField(Item, on_delete = models.CASCADE)
    returned_quantity = models.IntegerField()

    def __str__(self):
        return f"ReturnedItem: {self.item.item_brand}: {returned_quantity} pcs"

