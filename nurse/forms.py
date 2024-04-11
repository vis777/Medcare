from django import forms
from nurse.models import *
from autherization.models import *
from tempus_dominus.widgets import DatePicker
from django.core.exceptions import ValidationError
from django.utils import timezone


class BookingForm(forms.ModelForm):
    class Meta:
        model = NurseBooking
        fields = ['date', 'duration']
        

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['nurse'].queryset = Nurse.objects.all()

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date <= timezone.now().date():
            raise ValidationError('Date must be in the future.')
        return date    


        
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['user', 'date', 'details']  












from .models import Nurse

class NurseProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=False)
    name = forms.CharField(label='Name', required=False)

    class Meta:
        model = Nurse
        fields = [ 'phone', 'name', 'email', 'image', 'profile', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(NurseProfileUpdateForm, self).__init__(*args, **kwargs)
        if self.instance.user:
            self.initial['name'] = self.instance.user.name
            self.initial['email'] = self.instance.user.email

    def save(self, commit=True):
        nurse = super().save(commit=False)
        if commit:
            nurse.save()
        return nurse
