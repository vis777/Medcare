from django.urls import path
from .views import *

urlpatterns = [
    path('clinical_base/', clinical_base),
    path('device_page/', devicepage, name='device_page'),
    
    path('add_device/', add_device, name="add_device"),
    path('success/', upload_succes, name="upload_success"),
    path("device_display/<int:id>/", device_display, name="device_display"),
    path("device_delete/<int:id>/", device_delete, name="device_delete"),
    path("device_update/<int:id>/", device_update, name="device_update"),
    
    path('device/<int:device_id>/', device_detail, name='device_detail'),
]