from django.db import models

# Create your models here.
class Supplier(models.Model):
    supplier_name = models.CharField(max_length = 300, primary_key = True)
    supplier_phone_number = models.CharField(max_length = 300)
    def __str__(self):
        return f"{self.supplier_name}"
