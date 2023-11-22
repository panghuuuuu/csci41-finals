from django.db import models

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

    item_number = models.AutoField(primary_key = True, Unique = True)
    item_brand = models.CharField(max_length = 300)
    item_model = models.CharField(max_length = 300)
    item_qty = models.IntegerField()
    item_type = models.CharField(max_length = 300, choices = ITEM_TYPE_CHOICES)
    item_cost = models.DecimalField(max_digits = None, decimal_places = 3) #not sure if none
    item_SRP = models.DecimalField(max_digits = None, decimal_places = 3) #not sure if none
    item_total_cost = models.DecimalField(max_digits = 10, decimal_places = 2, editable = False)

    def save(self, *args, **kwargs):
        self.total_cost = self.item_total_cost * self.item_qty
        super().save(*args, **kwargs)

class SoldItem(models.Model):
    item = models.OneToOneField(Item, on_delete = models.CASCADE)
    sold_quantiy = models.IntegerField()

    def save(self, *args, **kwargs):
        self.total_sales = self.sold_quantity * self.item_total_cost
    
    def __str__(self):
        return f"SoldItem: {self.item.item_brand} {self.item.item_model}"

class DeliveredItem(models.Model):
    item = models.OneToOneField(Item, on_delete = models.CASCADE)
    delivered_quantity = models.IntegerField()

    def __str__(self):
        return f"DeliveredItem: {self.item.item_brand} {self.item.item_model}"

class IssuedItem(models.Model):
    item = models.OneToOneField(Item, on_delete = models.CASCADE)
    issued_quantity = models.IntegerField()

    def __str__(self):
        return f"IssuedItem: {self.item.item_brand} {self.item.item_model}"

class ReturnedItem(models.Model):
    item = models.OneToOneField(Item, on_delete = models.CASCADE)
    quantity_returned = models.IntegerField()

    def __str__(self):
        return f"ReturnedItem: {self.item.item_brand} {self.staff.item_model}"

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
