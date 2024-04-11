from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class NormalUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)
    is_shop = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    profile = models.TextField(null=True, blank=True)
    address=models.CharField(max_length=100, null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    
    

class Customer(models.Model):
    user = models.OneToOneField(NormalUser, on_delete=models.CASCADE, primary_key=True) 
    phone = models.CharField(max_length=20)
    address=models.CharField(max_length=200)
    def __str__(self):
        return self.user.username


class Nurse(models.Model):
    user = models.OneToOneField(NormalUser, on_delete=models.CASCADE, primary_key=True)
    license_number = models.CharField(max_length=20,unique=True)
    phone = models.IntegerField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    profile = models.TextField(null=True, blank=True)
    address=models.CharField(max_length=100, null=True, blank=True)
    is_active=models.BooleanField(default=False,null=True)
    is_available = models.BooleanField(default=True, null=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.user.username
    
class Shop(models.Model):
    owner = models.OneToOneField(NormalUser, on_delete=models.CASCADE, null=True,blank=True)
    shop_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    def __str__(self):
        return self.owner.username


