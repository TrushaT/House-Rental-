from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator 
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)

class Tenant(models.Model):

    MARITIAL_STATUS_CHOICES = [
        ('Single','Single'),
        ('Married','Married'),
    ]

    OCCUPATION_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Doctor', 'Doctor'),
        ('Enterepreneur', 'Enterepreneur')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    maritial_status = models.CharField(max_length=10,choices=MARITIAL_STATUS_CHOICES)
    Occupation = models.CharField(max_length=200, choices=OCCUPATION_CHOICES)
    phone_number = PhoneNumberField(blank = False)

    def __str__(self):
        return self.user.username

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class Property(models.Model):

    size_choices = [
        ('1 BHK' ,'1 BHK'),
        ('2 BHK' ,'2 BHK'),
        ('3 BHK' ,'3 BHK'),
        ('4 BHK' ,'4 BHK')
    ]

    area_choices = [
        ('Borivali' ,'Borivali'),
        ('Kandivali' ,'Kandivali'),
        ('Malad' ,'Malad'),
        ('Goregaon' ,'Goregaon')
    ]

    property_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    property_size = models.CharField(choices=size_choices, max_length = 100)
    monthly_rent = models.PositiveIntegerField(validators = [MinValueValidator(1)])
    property_image = models.ImageField(default='default.jpg',upload_to='property_images/',blank = False)
    area = models.CharField(choices=area_choices, max_length = 100)
    address_line_1 = models.CharField(max_length = 100)
    address_line_2 = models.CharField(max_length = 100)

    def __str__(self):
        return "Property" + str(self.id)

class BookMarkPropertyList(models.Model):

    list_owner = models.OneToOneField(Tenant,on_delete = models.CASCADE)
    bookmarked_properties = models.ManyToManyField(Property, blank=True)

    def __str__(self):
        return str(self.list_owner.user.username) + " BookMarkPropertyList"