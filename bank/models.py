from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from datetime import timedelta

# Custom User model
class User(AbstractUser):
    phone_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    account_number = models.CharField(max_length=50, unique=True, null=True)
    state = models.CharField(max_length=50, default="active")



class Transfer(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('User', on_delete=models.CASCADE)  # Foreign key to the User model
    amount = models.FloatField()
    state = models.CharField(max_length=50)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return f"Transfer {self.id} - User {self.id_user} - {self.amount} ({self.state})"
    
class Code(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit id field
    id_transfer = models.ForeignKey('Transfer', on_delete=models.SET_NULL, null=True)  # Foreign key to Transfer model
    code = models.CharField(max_length=100, unique=True)  # Unique code field
    date_expire = models.DateTimeField(default=now() + timedelta(days=7))  # Expiration date (default to 7 days from now)

    def __str__(self):
        return f"Code {self.id} - Transfer {self.id_transfer_id} - {self.code} (Expires: {self.date_expire})"
    
class Solicitude(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit ID field
    id_user = models.ForeignKey('User', on_delete=models.CASCADE)  # Foreign key to User model
    amount = models.FloatField()  # The requested amount
    deadlines = models.IntegerField()  # Deadline (e.g., in days or months)
    income = models.FloatField()  # User's income
    company = models.CharField(max_length=255)  # Name of the company the user works in
    time_working = models.IntegerField(help_text="Time working in months")  # Duration in current job (in months)
    date = models.DateTimeField(default=now)  # Date the solicitude was created
    state = models.CharField(max_length=50, choices=[
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
        ('completed', 'completed'),
    ], default='pending')  # State of the loan

    def __str__(self):
        return f"Solicitude {self.id} - User {self.id_user_id} - {self.amount} ({self.date})"
    
class Loan(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit ID field
    id_user = models.ForeignKey('User', on_delete=models.CASCADE)  # Foreign key to User model
    amount = models.FloatField()  # Loan amount
    deadlines = models.IntegerField(help_text="Deadlines in months")  # Deadline in months
    date = models.DateTimeField(default=now)  # Date the loan was created
    date_expire = models.DateTimeField(null=True, blank=True, help_text="Expiration date of the loan")  # Expiry date
    state = models.CharField(max_length=50, choices=[
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
        ('completed', 'completed'),
    ], default='pending')  # State of the loan

    def save(self, *args, **kwargs):
        # Automatically calculate `date_expire` based on `deadlines` if not set
        if not self.date_expire and self.deadlines:
            self.date_expire = self.date + timedelta(days=self.deadlines * 30)  # Approx. 30 days per month
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan {self.id} - User {self.id_user_id} - {self.amount} ({self.state})"