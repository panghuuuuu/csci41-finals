from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from supplier.models import Supplier
from client.models import Client
from agent.models import Agent
class Staff(models.Model):
    REGULAR = 'Regular'
    ISSUER = 'Issuer'
    RECEIVER = 'Receiver'

    STAFF_TYPE_CHOICES = [
        (REGULAR, 'Regular'),
        (ISSUER, 'Issuer'),
        (RECEIVER, 'Receiver'),
    ]

    staff_number = models.AutoField(primary_key=True, unique=True)
    staff_first_name = models.CharField(max_length=300)
    staff_last_name = models.CharField(max_length=300)
    staff_phone_number = models.IntegerField()
    staff_type = models.CharField(max_length=300, choices=STAFF_TYPE_CHOICES)

    def __str__(self):
        return f"{self.staff_last_name}, {self.staff_first_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.staff_type == 'Receiver':
            Receiver.objects.create(staff=self)
            user, created = User.objects.get_or_create(username=str(self.staff_number))
            print(f"User created: {created}, username: {user.username}")

            user.first_name = self.staff_first_name
            user.last_name = self.staff_last_name
            user.email = f"{self.staff_number}@example.com" 
            user.set_unusable_password()  
            user.set_password(f"{self.staff_first_name}12345")
            user.save()
        elif self.staff_type == 'Issuer':
            Issuer.objects.create(staff=self)
class Receiver(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    receiver_number = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.staff.staff_last_name}, {self.staff.staff_first_name}"

class Issuer(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    issuer_number = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.staff.staff_last_name}, {self.staff.staff_first_name}"

class Order(models.Model):
    order_number = models.AutoField(primary_key=True, unique=True)
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE, null=False, blank=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False, blank=False)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    isDelivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order_number} {self.order_date} {self.order_time}"

class BatchInventory(models.Model):
    batch_number = models.AutoField(primary_key=True, unique=True)
class Issuance(models.Model):
    batch_number = models.ForeignKey(BatchInventory, on_delete=models.CASCADE, null=False, blank=False)
    issuer = models.ForeignKey(Receiver, on_delete=models.CASCADE, null=False, blank=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    issue_date = models.DateField(auto_now_add=True)
    issue_time = models.TimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def verify_agent(self):
        if self.agent.client != self.client:
            raise ValidationError("Agent client does not match specified client.")

