from django.urls import path,include
from .views import *

urlpatterns=[

    path("add/<int:id>/", add_to_cart, name="add_to_cart"),
    path("cart_view/", cart_view, name="cart_view"),
    path('cart/remove/<int:id>/', devremove_cart_item, name='removeitem'),
    path("cart/placeprer/",OrderForm,name="orderitem"),
    path("cart/order_confirm/", order_confirm_view, name="order_confirm_view"),

    path('add-to-cart/<int:id>/', medadd_to_cart, name='med_to_cart'),
    path('cart/', medcart_view, name='med_cart_view'), 
    path('cart/remove-from-cart/<int:id>/', remove_cart_item, name='remove_cart_item'), 
    path("cart/medorder/",MedorderForm,name="medorder"),
    path("cart/payment/", medorder_confirm_view, name="payment"),
    path("cart/itemremove/<int:id>/",itemcart_remove , name="itemremove"),

]