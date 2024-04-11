from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from .models import *
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .models import Medcart, Medicine_inventory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.http import HttpResponseBadRequest

@login_required
def add_to_cart(request, id):
    try:
        device = DeviceInformation.objects.get(id=id)
        print(device)
    except DeviceInformation.DoesNotExist:
        return HttpResponseNotFound("Device does not exist")

    user = request.user
    
    existing_cart_item = Divicecart.objects.filter(user=user, device=device).first()
    if existing_cart_item:
        
        existing_cart_item.quantity = 1
        existing_cart_item.save()
    else:
      
        cart = Divicecart.objects.create(user=user, device=device,quantity=1)
        cart.save()
    
    
    
    
    return redirect("cart_view")

def cart_view(request):
    user= request.user
    cart = Divicecart.objects.filter(user=user)
    total = 0
    for i in cart:
        total += i.quantity * i.device.price

    return render(request, "cart/add_to_cart.html", {'cart': cart, 'total': total})

# 

from django.shortcuts import get_object_or_404


def devremove_cart_item(request, id):
    cart_item = get_object_or_404(Divicecart, id=id)

    cart_item.delete()

    return redirect('cart_view')


def OrderForm(request):
    if(request.method=="POST"):
        address=request.POST['address']
        phone=request.POST['phone']
        user=request.user
        cart=Divicecart.objects.filter(user=user)
        total=0
        for i in cart:
            total=total+i.quantity*i.device.price
            obj=Order.objects.create(user=user,address=address,phone=phone,device=i.device,no_of_items=i.quantity,order_status="paid", total_price=total)
            obj.save()
            i.device.delete()
        cart.delete()
        return redirect("order_confirm_view")

    return render(request,"cart/orderform.html")


def order_confirm_view(request):
    return render(request, "cart/order_confirm.html")







@login_required
def medadd_to_cart(request, id):
    user = request.user

    medicine = get_object_or_404(Medicine_inventory, id=id)
    try:
        cart_item = Medcart.objects.get(user=user, medicine=medicine)
        if cart_item.quantity < medicine.quanity_availble:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, "Sorry, this product is out of stock.")
    except Medcart.DoesNotExist:
        if medicine.quanity_availble > 0:
            cart_item = Medcart.objects.create(user=user, medicine=medicine, quantity=1)
            cart_item.save()
        else:
            messages.error(request, "Sorry, this product is out of stock.")
    return redirect('med_cart_view')


def med_cart_view(request):
    total = 0
    user = request.user
    cart = Medcart.objects.filter(user=user)
    for item in cart:
        total += item.quantity * item.medicine.price
    return render(request, 'medicine_cart_view.html', {'cart': cart, 'total': total})

def medcart_view(request):
    user = request.user
    cart = Medcart.objects.filter(user=user)
    total = 0
    for item in cart:
        total += item.subtotal()

    return render(request, "cart/medicine_cart_view.html", {'cart': cart, 'total': total})

def remove_cart_item(request, id):
    cart_item = get_object_or_404(Medcart, id=id)

    cart_item.delete()

    return redirect('med_cart_view')

def MedorderForm(request):
    if(request.method=="POST"):
        address=request.POST['address']
        phone=request.POST['phone']
        user=request.user
        cart=Medcart.objects.filter(user=user)
        total=0
        for i in cart:
            total=total+i.quantity*i.medicine.price
            obj=MedicineOrder.objects.create(user=user,address=address,phone=phone,medicine=i.medicine,no_of_items=i.quantity,order_status="paid", total_price=total)
            obj.save()
            i.medicine.delete()
        cart.delete()
        return redirect("payment")

    return render(request,"cart/orderform.html")


def medorder_confirm_view(request):
    return render(request, "cart/medpayment.html")

from django.http import JsonResponse

def itemcart_remove(request,id):
    try:
        med = Medicine_inventory.objects.get(id=id)
        print(med)
    except Medicine_inventory.DoesNotExist:
        raise Http404("Medicine inventory with id {} does not exist".format(id))
    # product=Medicine_inventory.objects.get(id=id)
    user=request.user
    try:
        cart=Medcart.objects.get(user=user,medicine=med)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()

        else:
            cart.delete()

    except:
        pass
    return redirect('med_cart_view')
