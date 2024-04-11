
from django import forms
from autherization.models import *
from medicines.models import Medicine_Category, Medicine_inventory

class CategoryCreateForm(forms.ModelForm):
    

    class Meta:
        model=Medicine_Category
        fields=["category_name"]


class AddMedicineForm(forms.ModelForm):

    class Meta:
        model=Medicine_inventory
        fields = ['medicine_name', 'expiry_date', 'manufacturer', 'quanity_availble', 'price', 'image','category']

        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'})
        }




   



    def clean_medicine_name(self):
       medicine_name = self.cleaned_data.get('medicine_name')
       if not  medicine_name:
            raise forms.ValidationError("Name cannot be empty")
       return  medicine_name

   

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be a positive number")
        
        return price     
    
class ShopProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Shop
        fields = ['phone', 'location', 'shop_name']