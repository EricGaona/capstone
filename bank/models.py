from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from datetime import timedelta

# Custom User model
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    account_number = models.CharField(max_length=50, unique=True, null=True)
    state = models.CharField(max_length=50, default="active")
    balance = models.FloatField(default=0.0)



class Transfer(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('User', on_delete=models.CASCADE)  # Foreign key to the User model
    amount = models.FloatField()
    state = models.CharField(max_length=50)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return f"Transfer {self.id} - User {self.id_user} - {self.amount} ({self.state})"
    
