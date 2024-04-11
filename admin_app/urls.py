from django.urls import path
from . import views

urlpatterns = [
    path("admin_app/device_list/", views.device_list, name="device_list"),
    path("admin_app/device_approval/<int:id>/", views.device_approval, name="device_approval"),

    path("admin_app/nurse_list/", views.nurse_list, name="nurse_list"),
    path("admin_app/nurse_approval/<int:id>/", views.nurse_approval, name="nurse_approval"),
]