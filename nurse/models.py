from django.db import models
from django.contrib.auth.models import User
from autherization.models import *
# Create your models here.



class NurseBooking(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE,related_name='Nurse',null=True, default=0)
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE,related_name='user', null=True, default=0)
    date = models.DateField()
    duration = models.IntegerField() 
    is_active = models.BooleanField(default=False, null=True)
    
    def __str__(self):
        return self.user.username





class Report(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)  # Assuming this is the user who is generating the report
    date = models.DateField()
    details = models.TextField()