from django.shortcuts import render,redirect, get_object_or_404
from nurse.forms import *
from clinical_devices.models import *
from django.core.mail import send_mail
from django.conf import settings
from autherization.models import *
from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView,TemplateView,View
from nurse.models import *
from django.contrib import messages

# Create your views here.
def device_list(request):
    devices = DeviceInformation.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, "admin/device_list.html", {'device_list': devices})

def device_approval(request, id):
    device = get_object_or_404(DeviceInformation, id=id)
    device.is_approved = True
    device.save()
    messages.success(request, "Device approved successfully!")
    return redirect('device_list')

def unapprove_device(request, id):
    device = get_object_or_404(DeviceInformation, id=id)
    device.is_approved = False
    device.save()
    messages.info(request, "Device has been unapproved.")
    return redirect('device_list')

def delete_device(request, id):
    device = get_object_or_404(DeviceInformation, id=id)
    device.delete()
    messages.success(request, "Device deleted successfully.")
    return redirect('device_list')

# def device_approval(request, id):

#     device = DeviceInformation.objects.get(id=id) 
#     user_name = device.user.username
#     user_email = device.user.email
#     device.is_approved=True
#     device.save()
#     subject = "Approval Confirmation"
#     message = (
#         f"Hi {user_name},\n\n"
#         "Congratulations! Your device upload request has been approved. "
#         "You can now access and manage your device.\n\n"
#         "Thank you for choosing us.\n\n"
#         "Best regards,\n"
#         "CareLink"
#     )
#     email_from = "carelink30@gmail.com"
#     email_to = user_email
#     send_mail(subject, message, email_from, [email_to])

#     return redirect('device_list')


# class NurseListView(ListView):
#     model = Nurse
#     template_name = 'admin/nurselist.html'  
#     context_object_name = 'nurses'

# def nurse_list(request):
#     nurse = Nurse.objects.filter(is_active=False)
#     return render(request, "admin/nurselist.html", {'nurse_list': nurse})

# class NurseListView(ListView):
#     model = Nurse
#     template_name = 'admin/nurselist.html'  
#     context_object_name = 'nurses'

    # def get_queryset(self):
    #     return Nurse.objects.filter(is_active=False)


# def nurse_approval(request, id):
#     nurse = Nurse.objects.get(user_id=id)
#     user_name = nurse.user.username
#     user_email = nurse.user.email
#     nurse.is_active = True  # Set approved
#     nurse.save()

#     subject = "Welcome to the CareLink Family!"
#     message = (
#         f"Dear {user_name},\n\n"
#         "We are thrilled to welcome you to the CareLink family! Your request has been approved, and you are now an integral part of our team.\n\n"
#         "At CareLink, we value your commitment to providing exceptional care and support. Your dedication is truly appreciated.\n\n"
#         "Thank you for choosing CareLink. We look forward to working together to make a positive impact on the lives of those we serve.\n\n"
#         "Best regards,\n"
#         "The CareLink Team"
#     )

#     send_mail(subject, message, 'carelink30@gmail.com', [user_email])
#     return redirect('nurse_list')

def nurse_list(request):
    # Fetch all nurses (both approved and unapproved)
    nurses = Nurse.objects.all().order_by('-user__date_joined')
    return render(request, "admin/nurselist.html", {'nurse_list': nurses})

def nurse_approval(request, user_id):
    nurse = get_object_or_404(Nurse, user_id=user_id)
    nurse.is_active = True
    nurse.save()
    messages.success(request, "Nurse approved successfully!")
    return redirect('nurse_list')

def nurse_unapprove(request, user_id):
    nurse = get_object_or_404(Nurse, user_id=user_id)
    nurse.is_active = False
    nurse.save()
    messages.info(request, "Nurse has been unapproved.")
    return redirect('nurse_list')

def delete_nurse(request, user_id):
    nurse = get_object_or_404(Nurse, user_id=user_id)
    nurse.delete()
    messages.success(request, "Nurse deleted successfully.")
    return redirect('nurse_list')


def nurse_unapprove(request, id):
    nurse = Nurse.objects.get(user_id=id)
    nurse.is_active = False
    nurse.save()

    return redirect('nurse_list')

