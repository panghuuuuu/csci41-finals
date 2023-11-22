from django.db import models

# Create your models here.
class Agent(models.Model):
    agent_number = models.AutoField(primary_key = True, Unique = True)
    agent_first_name = models.CharField(max_length = 300)
    agent_last_name = models.CharField(max_length = 300)
    agent_phone_number = models.IntegerField()
