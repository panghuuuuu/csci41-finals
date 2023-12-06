from django.db import models
from client.models import Client
# Create your models here.
class Agent(models.Model):
    agent_number = models.AutoField(primary_key=True, unique=True)
    agent_first_name = models.CharField(max_length = 300)
    agent_last_name = models.CharField(max_length = 300)
    agent_phone_number = models.IntegerField()

    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.agent_last_name}, {self.agent_first_name}"

class Sales(models.Model):
    invoice_number = models.AutoField(primary_key=True, unique=True)
    agent = models.ForeignKey("Agent", on_delete=models.RESTRICT)
    sales_date = models.DateField(auto_now_add=True)
    total_sales = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return f"{self.invoice_number}: {self.agent}"
