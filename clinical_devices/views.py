from django.shortcuts import render,redirect
from .forms import *
from django.http import HttpResponse
from django.views.generic import DetailView


# Create your views here.
def clinical_base(request):
    
    return render(request, "clinical_base.html")


def add_device(request):
    if request.method == "POST":
        device = DeviceInformationForm(request.POST, request.FILES)
        if device.is_valid():
            pnm = device.cleaned_data['product_name']
            snm = device.cleaned_data['seller_name']
            desc =device.cleaned_data['description']
            ph = device.cleaned_data['phone']
            pr = device.cleaned_data['price']
            img = device.cleaned_data['product_image']
            devices = DeviceInformation(product_name=pnm, seller_name=snm, description=desc, phone=ph, price=pr, product_image=img, user=request.user)
            devices.save()    
            
            return redirect("upload_success")
        else:
            return HttpResponse("Oops! Upload failed.")
    return render(request, "clinical_devices/add_device.html") 

def upload_succes(request):
    return render(request, "clinical_devices/upload_success.html")    


# def devicepanel(request):
#     device_list = DeviceInformation.objects.filter(is_approved=True).order_by('-created_at')
#     return render(request, "clinical_devices/devicepanel.html", {"device_list": device_list})

def devicepage(request):
    device_list = DeviceInformation.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, "clinical_devices/device_page.html", {"device_list": device_list})


def device_display(request, id):
    device_info = DeviceInformation.objects.filter(user=id, is_approved=True).order_by('-created_at')
    return render(request, "clinical_devices/my_devices.html", {"device_info": device_info})


def DeviceDetails(request, id):
    device_info = DeviceInformation.objects.filter(id=id).order_by('-created_at')
    return render(request, "clinical_devices/detail_device.html", {"devices": device_info})

def device_delete(request, id):
    a = DeviceInformation.objects.get(id=id)
    user_id = request.user.id
    a.delete()
    return redirect("device_display", id=user_id)


def device_update(request, id):
    device = DeviceInformation.objects.get(id=id)
    device.is_approved = False
    user_id = request.user.id
    
    form = DeviceForm(instance=device)
    
    if request.method == "POST":
        form = DeviceForm(request.POST, request.FILES, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_display', id=user_id )
    
    return render(request, "clinical_devices/edit_device.html", {'form': form})






