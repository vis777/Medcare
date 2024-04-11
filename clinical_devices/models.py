from django.db import models
from autherization.models import *

# Create your models here.
class DeviceInformation(models.Model):
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE,null=True,blank=True)
    product_name = models.CharField(max_length=200)
    seller_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    product_image = models.ImageField(upload_to="images/", null=False,blank=False)
    phone = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=0)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return self.product_name
    
# class ApprovedDeviceInformation(models.Model):
#     uid = models.IntegerField()
#     product_name = models.CharField(max_length=200)
#     seller_name = models.CharField(max_length=100)
#     description = models.CharField(max_length=1000)
#     product_image = models.FileField(upload_to="images/", null=False,blank=False)
#     phone = models.IntegerField()
#     price = models.DecimalField(max_digits=12, decimal_places=2)


