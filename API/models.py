import uuid
from django.db import models
from django.conf import settings
from .managers import CustomUserManager
from django_userforeignkey.models.fields import UserForeignKey
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin




GENDER = [
    ('MALE', 'male'),
    ('FEMALE', 'female'),
    ]


class CustomUser(AbstractBaseUser,PermissionsMixin):
    full_name = models.CharField(max_length=255, blank=False)
    email_address = models.EmailField(max_length=255,unique=True,blank=False)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=13, choices=GENDER, default='FEMALE')
    country = models.CharField(max_length=255, blank=True)
    productID = models.CharField(max_length=255,unique=True, primary_key=True,default=uuid.uuid4)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'productID'
    REQUIRED_FIELDS = ['email_address','full_name']

    def __str__(self):
        return self.email_address

    def has_perm(self, perm, obj=None):
        return True
    
    def has_perms(self, perm, obj=None):
        return True
    

    def has_module_perm(self, app_label):
        return app_label
    

    def has_module_perms(self, app_label):
        return app_label

class SensorData(models.Model):
    """ THIS HOLDS THE RECORDS OF THE SENSOR DATA OVER TIME """
    smoke = models.FloatField(default = 0)
    alcohol = models.FloatField(default = 0)
    lpg_gas = models.FloatField(default = 0)
    hydrogen = models.FloatField(default = 0)
    humidity = models.FloatField(default = 0)
    temperature = models.FloatField(default = 0)
    carbon_dioxide = models.FloatField(default = 0)
    carbon_monoxide = models.FloatField(default = 0)
    air_quality_index = models.FloatField(default = 0)
    productID = UserForeignKey(auto_user_add=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

class RiskAlert(models.Model):
    """ THIS HOLDS THE RISK ALERTS BASED ON THE SENSOR DATA OVER TIME """
    element = models.CharField(max_length=255)  # e.g., "Carbon Dioxide"
    threshold_high = models.FloatField()  # High threshold for alert
    threshold_bad = models.FloatField()  # Very high threshold for bad alert
    danger_message = models.TextField()  # Danger message for this element
    solution_message = models.TextField()  # Solution message for this element
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

class HealthTip(models.Model):
    """ THIS HOLDS THE HEALTH TIPS OVER TIME """
    title = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True,null=True)   