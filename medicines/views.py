from django.shortcuts import render
from medicines.forms import *
# Create your views here.
from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView,TemplateView,View
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from medicines.models import *
from medicines.forms import CategoryCreateForm,AddMedicineForm
from django.http import HttpResponse
from datetime import date
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from autherization.models import *
from django.db.models import Q
from clinical_devices.models import DeviceInformation 
from autherization.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
class CategoryCreateView(CreateView,ListView):

    template_name="medicines/add_category.html"
    form_class=CategoryCreateForm
    model=Medicine_Category
    context_object_name="categories"
    success_url=reverse_lazy("add-category")

    def form_valid(self, form):
        messages.success(self.request,"category added successfully")

        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"category adding failed")
        return super().form_invalid(form)
def remove_category(request,*args,**kwargs):
    id=kwargs.get("pk")
    Medicine_Category.objects.filter(id=id).delete()
    messages.success(request,"category removed")
    return redirect("add-category")




# class MedicineAddView(CreateView):
#     template_name = "medicines/add_medicines.html"
#     form_class = AddMedicineForm
#     success_url = reverse_lazy("shoppanel")

#     def form_valid(self, form):
#         messages.success(self.request,"medicine added successfully")

#         return super().form_valid(form)
    
#     def form_invalid(self, form):
#         messages.error(self.request,"medicine adding failed")
#         return super().form_invalid(form)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Medicine_Category.objects.all()
#         return context

class MedicineAddView(CreateView):
    template_name = "medicines/add_medicines.html"
    form_class = AddMedicineForm
    success_url = reverse_lazy("shoppanel")

    def form_valid(self, form):
        messages.success(self.request, "Medicine added successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)  # Debugging step
        messages.error(self.request, "Medicine adding failed")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Medicine_Category.objects.all()
        return context

    


class MedicineListView(ListView):
    template_name = "medicines/list_medicines.html"
    model = Medicine_inventory
    context_object_name = "medicines"
    ordering = ['-created_at']

    def get_queryset(self):
        return Medicine_inventory.objects.filter(quanity_availble__gt=0).order_by('-created_at')




def medicine_list(request):
    medicines = Medicine_inventory.objects.all()
    return render(request, 'shoppanel.html', {'medicines': medicines})



def search_medicines(request):
    query = request.GET.get('q')
    if query:
        medicines = Medicine_inventory.objects.filter(Q(medicine_name__icontains=query) | Q(manufacturer__icontains=query))
        devices = DeviceInformation.objects.filter(product_name__icontains=query)
        medicines = list(medicines) + list(devices)
    else:
        medicines = []
    return render(request, 'medicines/search_medicine.html', {'medicines': medicines, 'query':query})
                                                       


def remove_medicines(request,*args,**kwargs):
    id=kwargs.get("pk")
    Medicine_inventory.objects.filter(id=id).delete()
    messages.success(request,"medicine removed")
    return redirect("shoppanel")


class MedicineDetailView(DetailView):
    template_name="medicines/detail_medicine.html"
    model=Medicine_inventory
    context_object_name="medicines"

class MedicineUpdateView(UpdateView):
    template_name="medicines/change_medicines.html"
    model=Medicine_inventory
    form_class=AddMedicineForm
    success_url=reverse_lazy("shoppanel")
    def form_valid(self, form):
        messages.success(self.request," updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"updating failed")
        return super().form_invalid(form)
    



class ExpiredMedicinesView(TemplateView):
    template_name = 'medicines/expiredlist.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter expired medicines
        context['medicines'] = Medicine_inventory.objects.filter(expiry_date__lt=timezone.now())
        return context
    
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine_inventory, pk=pk)
    medicine.delete()
    return redirect('shoppanel')




# class ShopPanelView(TemplateView):
#     template_name = 'medicines/shoppanel.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['medicines'] = Medicine_inventory.objects.all()
#         context['categories'] = Medicine_Category.objects.all()
#         return context
        
      
# class ShopPanelView(TemplateView):
#     template_name = 'medicines/shoppanel.html'

#     @method_decorator(login_required)
#     @method_decorator(never_cache)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['medicines'] = Medicine_inventory.objects.all()
#         context['categories'] = Medicine_Category.objects.all()
#         return context     


@login_required
@never_cache
def shop_panel_view(request):
    context = {
        'medicines': Medicine_inventory.objects.all(),
        'categories': Medicine_Category.objects.all()
    }
    return render(request, 'medicines/shoppanel.html', context)


class BabyCareMedicinesView(TemplateView):
    template_name = 'medicines/babycare.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baby_care_category = Medicine_Category.objects.get(category_name='Baby Care')
        context['medicines'] = Medicine_inventory.objects.filter(category=baby_care_category)
        return context
    

class BabyCareDetailView(DetailView):
    template_name="medicines/babycare_detail.html"
    model=Medicine_inventory
    context_object_name="medicine"    
    
class BeautyCareMedicinesView(TemplateView):
    template_name = 'medicines/beautyandpersonelcare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        beauty_and_care_category =   Medicine_Category.objects.get(category_name='Beauty & Personal Care')
        context['medicines'] = Medicine_inventory.objects.filter(category=beauty_and_care_category)
        return context
    
class BeautyCareDetailView(DetailView):
    template_name = "medicines/beautyandpersonelcare_detail.html"  
    model=Medicine_inventory
    context_object_name="medicine"

    
class NutritionView(TemplateView):
    template_name = 'medicines/nutrition.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nutrition_and_care_category =   Medicine_Category.objects.get(category_name='Nutrition & Suppliments')    
        context['medicines'] = Medicine_inventory.objects.filter(category=nutrition_and_care_category )
        return context
    
class NutritionDetailView(DetailView):
    template_name = "medicines/nutrition_detail.html"  
    model=Medicine_inventory
    context_object_name="medicine"

    
class DiabetesView(TemplateView):
    template_name = 'medicines/diabetes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diabetes_category =   Medicine_Category.objects.get(category_name='Diabetes')    
        context['medicines'] = Medicine_inventory.objects.filter(category=diabetes_category)
        return context
    
class DiabetesDetailView(DetailView):
    template_name = "medicines/diabetes_detail.html"  
    model=Medicine_inventory
    context_object_name="medicine"    
    
class HairfallView(TemplateView):
    template_name = 'medicines/hairfall.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hairfall_category =Medicine_Category.objects.get(category_name='Hair Fall')
        context['medicines'] = Medicine_inventory.objects.filter(category= hairfall_category )
        return context
    

class HairfallDetailView(DetailView):
    template_name = "medicines/hairfall_detail.html"  
    model=Medicine_inventory
    context_object_name="medicine"   

def shop_profile(request):
    current_user = request.user
    
    try:
        shop_profile =  Shop.objects.get(owner=current_user)
        
    except Shop.DoesNotExist:
        shop_profile = None
        print("Shop profile does not exist for user:", current_user)
    
    context = {
        'shop_profile': shop_profile
    }
    
    return render(request, 'medicines/shopprofile.html',context)
                  

from autherization.models import Shop





class ShopProfileUpdateView(UpdateView):
    model = Shop
    form_class = ShopProfileUpdateForm  
    template_name = 'medicines/updateshop.html'
    success_url = reverse_lazy('shop_profile')  
    context_object_name="shop_profile"
    def get_object(self, queryset=None):
        return Shop.objects.get(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.user.email
        return context
    

    def form_valid(self, form):
        
        form.instance.owner = self.request.user
        self.request.user.email = form.cleaned_data['email']
        
        self.request.user.save()
        print('email')
       
        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Failed to update profile")
        return super().form_invalid(form)
