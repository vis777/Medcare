from autherization.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from autherization.views import *
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView,TemplateView,View
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from autherization.forms import *
from django.views.generic import TemplateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.cache import never_cache
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
import logging
from datetime import datetime, timedelta, date
from django.utils import timezone


# Create your views here.


@login_required
@never_cache
def nurse_panel_view(request):
    return render(request, 'Nurse/nursepanel.html')


def nurse_profile(request):
    # Retrieve the current logged-in user
    current_user = request.user
    
    # Query the Nurse model to get the nurse profile associated with the current user
    try:
        nurse_profile = Nurse.objects.get(user=current_user)


    except Nurse.DoesNotExist:
        # Handle the case where the nurse profile does not exist
        nurse_profile = None
    
    # Pass the nurse profile data to the template context
    context = {
        'nurse_profile': nurse_profile
    }
    
    # Render the template with the provided context
    return render(request, 'Nurse/nurse_profile.html',context)



def remove_profile(request,*args,**kwargs):
   id=kwargs.get("pk")
   Nurse.objects.filter(id=id).delete()
   messages.success(request,"Profile removed")
   return redirect("nursepanel")




from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class NurseProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Nurse
    form_class = NurseProfileUpdateForm
    template_name = 'Nurse/change_profile.html'
    success_url = reverse_lazy('nursepanel')
    context_object_name = "nurse_profile"

    def get_object(self, queryset=None):
        return Nurse.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.user.email
        context['name'] = self.request.user.name
        return context

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['email'] = user.email
        initial['name'] = user.name
        return initial  # <-- Make sure to return initial dictionary

    def form_valid(self, form):
        nurse_profile = form.save(commit=False)
        
        # Check if a new image was uploaded
        if 'profile_image' in self.request.FILES:
            nurse_profile.profile_image = self.request.FILES['profile_image']
        
        nurse_profile.save()

        # Update user model fields
        self.request.user.email = form.cleaned_data['email']
        self.request.user.name = form.cleaned_data['name']
        self.request.user.save()

        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update profile")
        return super().form_invalid(form)


class NurseListView(ListView):
    model = Nurse
    template_name = 'Nurse/profile.html'
    context_object_name = 'nurses'

    def get_queryset(self):
        return Nurse.objects.filter(is_active=True)

    

# 
    

# class NurseDetailView(View):
#     def get(self,request,pk):
#         nurse_obj = Nurse.objects.get(user__id= pk)
#         if nurse_obj.available_from and nurse_obj.available_from <= date.today():
#             nurse_obj.is_available = True
#             nurse_obj.available_from = None
#             nurse_obj.save()
#         context = {
#             "nurse":nurse_obj
#         }
#         return render(request,'Nurse/nurseprofile_for_user.html',context)
from datetime import date, timedelta
from django.shortcuts import get_object_or_404

class NurseDetailView(View):
    def get(self, request, pk):
        nurse_obj = get_object_or_404(Nurse, user__id=pk)

        # Check the latest active booking for this nurse
        active_booking = NurseBooking.objects.filter(nurse=nurse_obj, is_active=True).order_by('-date').first()

        if active_booking:
            booking_end_date = active_booking.date + timedelta(days=active_booking.duration * 30)

            if date.today() > booking_end_date:
                nurse_obj.is_available = True
                nurse_obj.save()

                active_booking.is_active = False
                active_booking.save()
            else:
                nurse_obj.is_available = False
                nurse_obj.save()
        else:
            nurse_obj.is_available = True
            nurse_obj.save()

        # Check if the logged-in user has booked this nurse
        user_booking = NurseBooking.objects.filter(nurse=nurse_obj, user=request.user, is_active=True).first()

        context = {
            "nurse": nurse_obj,
            "user_booking": user_booking
        }
        return render(request, 'Nurse/nurseprofile_for_user.html', context)




# class CreateBookingView(View):
#     def get(self, request, pk=None):
#         form = BookingForm()
#         return render(request, 'Nurse/booking.html', {'form': form})
    
#     def post(self, request, pk=None):
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             date = form.cleaned_data['date']
#             duration = form.cleaned_data['duration']
#             user = request.user
#             nurse = Nurse.objects.get(user__id=pk) if pk else None
            
#             try:
#                 c_booking = NurseBooking.objects.filter(user=user, nurse=nurse).latest('date')
#                 expiry_date = c_booking.date + relativedelta(days=30*duration)  
#                 print(expiry_date,'===========')
                
#                 if date < expiry_date:
#                     booking = NurseBooking.objects.create(user=user, nurse=nurse, date=date, duration=duration)
#                     booking.save()
#                     messages.success(request, 'Booking successful!')
#                     return redirect('customerpanel')
#                 else:
#                     messages.error(request, 'Booking not permitted. Existing booking date is not before the new booking date.')
#             except NurseBooking.DoesNotExist:
#                 booking = NurseBooking.objects.create(user=user, nurse=nurse, date=date, duration=duration)
#                 booking.save()
#                 messages.success(request, 'Booking successful!')
#                 return redirect('customerpanel')
#         return render(request, 'Nurse/booking.html', {'form': form})
class CreateBookingView(View):
    def get(self, request, pk=None):
        form = BookingForm()
        return render(request, 'Nurse/booking.html', {'form': form})

    def post(self, request, pk=None):
        form = BookingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            duration = form.cleaned_data['duration']
            user = request.user
            nurse = get_object_or_404(Nurse, user__id=pk)

            # Calculate new booking end date
            new_booking_end_date = date + relativedelta(days=30 * duration)

            # Check for any overlapping active booking for this nurse
            active_booking = NurseBooking.objects.filter(nurse=nurse, is_active=True).first()

            if active_booking:
                current_booking_end_date = active_booking.date + relativedelta(days=30 * active_booking.duration)

                if date <= current_booking_end_date:
                    messages.error(request, 'This nurse is already booked during the selected period.')
                    return render(request, 'Nurse/booking.html', {'form': form})

            # Create new booking
            booking = NurseBooking.objects.create(
                user=user,
                nurse=nurse,
                date=date,
                duration=duration,
                is_active=True  # New booking is active by default
            )
            booking.save()

            # Update nurse availability
            nurse.is_available = False
            nurse.save()

            messages.success(request, 'Booking successful!')
            return redirect('customerpanel')

        return render(request, 'Nurse/booking.html', {'form': form})
class UnbookNurseView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(NurseBooking, id=booking_id, user=request.user, is_active=True)

        # Mark booking inactive
        booking.is_active = False
        booking.save()

        # Make nurse available again
        nurse = booking.nurse
        nurse.is_available = True
        nurse.save()

        messages.success(request, "You have successfully unbooked the nurse.")
        return redirect('customerpanel')
def bookingsuccess(request):
    return render(request,"Nurse/bookingsuccess.html")


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class NurseUserList(LoginRequiredMixin, ListView):
    model = NurseBooking
    template_name = 'Nurse/nursepanel.html'
    context_object_name = 'bookings'  # The variable used in the template

    def get_queryset(self):
        nurse = self.request.user.nurse  # Assuming Nurse has OneToOneField to User
        # Only get ACTIVE bookings
        return NurseBooking.objects.filter(nurse=nurse, is_active=True)







def request_approval(request,id):
    user = NurseBooking.objects.get(user_id=id) 
    user_name = user.user.username
    user_email = user.user.email
    user.is_active = True
    user.save()
    # nurse_id = request.user
    nurse = Nurse.objects.get(user=request.user)
    nurse.is_available = False
    
    nurse.save()
    subject = "Your Home Nurse Request Has Been Approved"
    message = (
        f"Dear {user_name},\n\n"
        "We are pleased to inform you that your request for a home nurse service has been approved!\n\n"
        "At CareLink, we are committed to providing you with the best possible care and support.\n\n"
        "Your assigned nurse will be in touch with you shortly to discuss the details of your care plan.\n\n"
        "Thank you for choosing CareLink. We look forward to assisting you in your journey to better health.\n\n"
        "Best regards,\n"
        "The CareLink Team"
    )
    email_from = "carelink30@gmail.com"
    email_to = user_email
    send_mail(subject, message, email_from, [email_to])
    return redirect('nursepanel')  



# def nurse_delete(request, id):
#     obj = Nurse.objects.get(user_id=id)
    
#     obj.delete()
#     return redirect("index")






def nurse_delete(request, id):
    try:
        obj = NormalUser.objects.get(id=id)
        print("Nurse object:", obj)  
        obj.delete()
        print("Nurse profile deleted successfully.") 
        return redirect("index")
    except NormalUser.DoesNotExist:
        print("Nurse profile does not exist.")  
        return redirect("index")  

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.conf import settings
import os

from .models import Nurse

def certificate_nurse(request, pk):
    nurse_profile = get_object_or_404(Nurse, pk=pk)
    context = {
        'nurse_profile': nurse_profile,
        'user': nurse_profile.user,
    }
    return render(request, 'Nurse/certificate_nurse.html', context)

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.conf import settings
import os

from .models import Nurse

def download_nurse_certificate(request, pk):
    nurse_profile = get_object_or_404(Nurse, pk=pk)


    logo_url = request.build_absolute_uri(settings.STATIC_URL + "images/carelink-high-resolution-logo-transparent.png")
    profile_img_url = request.build_absolute_uri(nurse_profile.image.url)  

   
    html_content = render_to_string('Nurse/certificate_nurse_pdf.html', {
        'nurse_profile': nurse_profile,
        'user': nurse_profile.user,
        'logo_url': logo_url,
        'profile_img_url': profile_img_url,
    })

    # Convert HTML to PDF
    pdf = HTML(string=html_content).write_pdf(
        stylesheets=[CSS(string="""
            body { font-family: 'Times New Roman', serif; text-align: center; }
            .certificate-container { border: 10px solid #23c4c4; padding: 30px; max-width: 800px; margin: auto; }
            .certificate-header img { width: 120px; }
            .profile-img { width: 150px; height: 150px; border-radius: 50%; border: 5px solid #23c4c4; }
            h1 { color: #23c4c4; font-size: 32px; }
            .info-label { font-weight: bold; color: #23c4c4; }
            .info-value { color: #555; }
        """)]
    )

    # Create HTTP response with the PDF file
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="nurse_certificate_{nurse_profile.pk}.pdf"'
    return response

    
