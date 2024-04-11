from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomerSignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=20)

    class Meta(UserCreationForm.Meta):
        model = NormalUser
        fields = ('username', 'email', 'phone', 'password1', 'password2','address')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Example@gmail.com'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),

        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
            customer = Customer.objects.create(user=user, phone=self.cleaned_data['phone'])
            customer.save()
        return user
    

class NurseSignUpForm(UserCreationForm):
    license_number = forms.CharField(max_length=20)
    phone = forms.IntegerField()
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}))
    image = forms.ImageField(required=False)  

    class Meta(UserCreationForm.Meta):
        model = NormalUser
        fields = ('username', 'name','email', 'license_number', 'password1', 'password2','image','profile','address','phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Example@gmail.com'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),       
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'profile' : forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your work experience'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
        }

    def save(self, commit=True):
        user = super(NurseSignUpForm, self).save(commit=False)  # Specify the class and instance
        user.is_nurse = True
        user.name = self.cleaned_data['name']  # Include this line
        user.image = self.cleaned_data.get('image')  # Include this line
        if commit:
          user.save()
          nurse = Nurse.objects.create(user=user, name=self.cleaned_data['name'], license_number=self.cleaned_data['license_number'], phone=self.cleaned_data['phone'], image=self.cleaned_data['image'], profile=self.cleaned_data['profile'], address=self.cleaned_data['address'])
          nurse.save()

          return user
   

class ShopSignUpForm(UserCreationForm):
    shop_name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    phone = forms.IntegerField()

    class Meta(UserCreationForm.Meta):
        model = NormalUser
        fields = ('username', 'email', 'shop_name', 'location', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Example@gmail.com'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'shop_name': forms.TextInput(attrs={'class': 'form-control'}),

        }
    def save(self, commit=True):
        owner = super().save(commit=False)
        owner.is_shop = True
        if commit:
            owner.save()
            shop = Shop.objects.create(owner=owner, shop_name=self.cleaned_data['shop_name'], location=self.cleaned_data['location'], phone=self.cleaned_data['phone'])
            shop.save()
        return owner


   

class AdminForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=100)    

# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=200)
#     password = forms.CharField(max_length=100)  

    