from django.db import models

# Create your models here.
class Medicine_Category(models.Model):

    category_name=models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.category_name
    

    
class Medicine_inventory(models.Model):
    medicine_name=models.CharField(max_length=200,unique=True)
    price=models.PositiveIntegerField()
    manufacturer=models.CharField(max_length=200)
    expiry_date=models.DateTimeField(null=True,blank=True)
    quanity_availble=models.PositiveIntegerField()
    category=models.ForeignKey( Medicine_Category,null=True,on_delete=models.SET_NULL)
    image=models.ImageField(upload_to="images/",null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    def __str__(self):
        return self.medicine_name


class Expirylist(models.Model):

    expmedicine_name=models.CharField(max_length=200,unique=True)
    expexpiry_date=models.DateTimeField(null=True,blank=True)

   