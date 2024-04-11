from django.urls import path
from .views import *

urlpatterns = [
    path('clinical_base/', clinical_base),
    path('device_page/', devicepage, name='device_page'),
    
    path('devicepanel/', add_device, name="devicepanel"),
    path('success/', upload_succes, name="upload_success"),
    path("device_display/<int:id>/", device_display, name="device_display"),
    path("device_delete/<int:id>/", device_delete, name="device_delete"),
    path("device_update/<int:id>/", device_update, name="device_update"),
    path("device_details/<int:id>/", DeviceDetails, name="device_details")
]