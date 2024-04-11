from django import forms
from .models import *


# class DeviceInformationForm(forms.forms):
#     product_name = forms.CharField(max_length=200)
#     seller_name = forms.CharField(max_length=100)
#     description = forms.CharField(max_length=1000)
#     product_image = forms.FileField()
#     phone = forms.IntegerField()
#     price = forms.DecimalField(max_digits=12, decimal_places=3)

class DeviceInformationForm(forms.ModelForm):
    class Meta:
        model = DeviceInformation
        fields = "__all__"
        



class DeviceForm(forms.ModelForm):
    class Meta:
        model = DeviceInformation
        fields = ["product_name","seller_name","description","product_image","phone","price"]
        widgets = {
        

            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'seller_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter seller name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Select an image'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),

        }