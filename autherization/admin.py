from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(NormalUser)
admin.site.register(Customer)
admin.site.register(Nurse)
admin.site.register(Shop)
