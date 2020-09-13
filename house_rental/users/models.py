from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)

class Tenant(models.Model):
    MARITIAL_STATUS_CHOICES = [
        ('Single','Single'),
        ('Married','Married'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    maritial_status = models.CharField(max_length=10,choices=MARITIAL_STATUS_CHOICES,default='Single')
    Occupation = models.CharField(max_length=200)

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


    