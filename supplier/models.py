from django.db import models
# Create your models here.
class Supplier(models.Model):
    supplier_name = models.CharField(max_length = 300, primary_key = True)
    supplier_phone_number = models.CharField(max_length = 300)
    def __str__(self):
        return f"{self.supplier_name}"

class Delivery(models.Model):
    delivery_number = models.AutoField(primary_key=True, unique=True)
    order = models.ForeignKey("staff.Order", on_delete=models.CASCADE, null=True, blank=True, related_name='delivered_items')
    delivery_date = models.DateField(auto_now_add=True)
    delivery_time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.delivery_number} {self.delivery_date}"
        