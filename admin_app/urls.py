from django.urls import path
from . import views

urlpatterns = [
    path("admin_app/device_list/", views.device_list, name="device_list"),
    path("admin_app/device_approval/<int:id>/", views.device_approval, name="device_approval"),
    
    # path("admin_app/device_approval/<int:id>/", views.device_approval, name="device_approval"),

    # path('devices/approve/<int:id>/', views.approve_device, name='approve_device'),
    path('devices/unapprove/<int:id>/', views.unapprove_device, name='unapprove_device'),
    path('devices/delete/<int:id>/', views.delete_device, name='delete_device'),

    # path("admin_app/nurse_list/", views.nurse_list, name="nurse_list"),
    # path("admin_app/nurse_approval/<int:id>/", views.nurse_approval, name="nurse_approval"),
    path('nurse-list/', views.nurse_list, name='nurse_list'),
    path('nurse-approve/<int:user_id>/', views.nurse_approval, name='nurse_approval'),
    path('nurse-unapprove/<int:user_id>/', views.nurse_unapprove, name='nurse_unapprove'),
    path('nurse-delete/<int:user_id>/', views.delete_nurse, name='delete_nurse'),
    
]