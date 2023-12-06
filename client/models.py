from django.db import models

# Create your models here.
class Client(models.Model):
    client_name = models.CharField(max_length = 300, primary_key = True)
    client_office_address = models.CharField(max_length = 300)
    client_email_address = models.EmailField(max_length = 254) 
    
    def __str__(self):
        return f"{self.client_name}"
