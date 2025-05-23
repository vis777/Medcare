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
from .models import Divicecart, Order
from autherization.models import Customer 
from django.db import transaction
import razorpay
import logging

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


# def OrderForm(request):
#     if(request.method=="POST"):
#         address=request.POST['address']
#         phone=request.POST['phone']
#         user=request.user
#         cart=Divicecart.objects.filter(user=user)
#         total=0
#         for i in cart:
#             total=total+i.quantity*i.device.price
#             obj=Order.objects.create(user=user,address=address,phone=phone,device=i.device,no_of_items=i.quantity,order_status="paid", total_price=total)
#             obj.save()
#             i.device.delete()
#         cart.delete()
#         return redirect("order_confirm_view")

#     return render(request,"cart/orderform.html")


def order_confirm_view(request):
    return render(request, "cart/order_confirm.html")



def OrderForm(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Make sure only logged-in users can place orders

    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        user = request.user

        try:
            customer = Customer.objects.get(user=user)  # Ensure customer exists for the logged-in user
        except Customer.DoesNotExist:
            # Redirect or show error if customer profile doesn't exist
            return redirect('profile_setup')  # Example URL to create profile

        # Update customer address and phone if needed
        customer.address = address
        customer.phone = phone
        customer.save()

        cart = Divicecart.objects.filter(user=user)

        total = 0
        for item in cart:
            total += item.quantity * item.device.price
            Order.objects.create(
                user=user,
                address=address,
                phone=phone,
                device=item.device,
                no_of_items=item.quantity,
                order_status="paid",
                total_price=item.quantity * item.device.price  # Store individual item price
            )
            item.device.delete()

        cart.delete()
        return redirect("order_confirm_view")

    return render(request, "cart/orderform.html")







@login_required
def medadd_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine_inventory, id=medicine_id)
    cart_item, created = Medcart.objects.get_or_create(user=request.user, medicine=medicine)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('med_cart_view')

def remove_one_item(request, medicine_id):
    medicine = get_object_or_404(Medicine_inventory, id=medicine_id)
    cart_item = get_object_or_404(Medcart, user=request.user, medicine=medicine)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('med_cart_view')

def remove_cart_item(request, id):
    cart_item = get_object_or_404(Medcart, id=id, user=request.user)
    cart_item.delete()
    return redirect('med_cart_view')

def med_cart_view(request):
    user = request.user
    cart = Medcart.objects.filter(user=user)
    total = sum(item.subtotal() for item in cart)

    return render(request, "cart/medicine_cart_view.html", {'cart': cart, 'total': total})
# def medadd_to_cart(request, id):
#     user = request.user

#     medicine = get_object_or_404(Medicine_inventory, id=id)
#     try:
#         cart_item = Medcart.objects.get(user=user, medicine=medicine)
#         if cart_item.quantity < medicine.quanity_availble:
#             cart_item.quantity += 1
#             cart_item.save()
#         else:
#             messages.error(request, "Sorry, this product is out of stock.")
#     except Medcart.DoesNotExist:
#         if medicine.quanity_availble > 0:
#             cart_item = Medcart.objects.create(user=user, medicine=medicine, quantity=1)
#             cart_item.save()
#         else:
#             messages.error(request, "Sorry, this product is out of stock.")
#     return redirect('med_cart_view')


# def med_cart_view(request):
#     total = 0
#     user = request.user
#     cart = Medcart.objects.filter(user=user)
#     for item in cart:
#         total += item.quantity * item.medicine.price
#     return render(request, 'medicine_cart_view.html', {'cart': cart, 'total': total})

# def medcart_view(request):
#     user = request.user
#     cart = Medcart.objects.filter(user=user)
#     total = sum(item.subtotal() for item in cart)

#     return render(request, "cart/medicine_cart_view.html", {'cart': cart, 'total': total})


# def remove_cart_item(request, id):
#     cart_item = get_object_or_404(Medcart, id=id)

#     cart_item.delete()

#     return redirect('med_cart_view')

# def MedorderForm(request):
#     if(request.method=="POST"):
#         address=request.POST['address']
#         phone=request.POST['phone']
#         user=request.user
#         cart=Medcart.objects.filter(user=user)
#         total=0
#         for i in cart:
#             total=total+i.quantity*i.medicine.price
#             obj=MedicineOrder.objects.create(user=user,address=address,phone=phone,medicine=i.medicine,no_of_items=i.quantity,order_status="paid", total_price=total)
#             obj.save()
#             i.medicine.delete()
#         cart.delete()
#         return redirect("payment")

#     return render(request,"cart/orderform.html")

from django.shortcuts import render, redirect
from django.db import transaction
from .models import Medcart, Order
from medicines.models import Medicine_inventory

def MedorderForm(request):
    if request.method == "POST":
        address = request.POST['address']
        phone = request.POST['phone']
        user = request.user

        cart = Medcart.objects.filter(user=user)

        if not cart.exists():
            return redirect("cart")

        try:
            with transaction.atomic():  # Ensure atomicity (all or nothing)
                for item in cart:
                    print(item)
                    total_price = item.quantity * item.medicine.price

                    # Create order
                    Order.objects.create(
                        user=user,
                        address=address,
                        phone=phone,
                        medicine=item.medicine,
                        no_of_items=item.quantity,
                        order_status="paid",
                        total_price=total_price
                    )

                    medicine = item.medicine
                    if medicine.quanity_availble >= item.quantity:
                        medicine.quanity_availble -= item.quantity
                        medicine.save()
                    else:
                        return render(request, "cart/orderform.html", {
                            "error": f"Not enough stock for {medicine.medicine_name}"
                        })

                # Clear the cart
                cart.delete()

            return redirect("payment")

        except Exception as e:
            return render(request, "cart/orderform.html", {
                "error": str(e)
            })

    return render(request, "cart/orderform.html")



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

@login_required
def paymentpage(request, cart_type):
    user = request.user
    order_currency = "INR"
    client = razorpay.Client(auth=("rzp_test_8ZlQ5ZrMiHMwmU", "f59o6eHBPsp6w3F2RW6ExcgZ"))

    # Initialize payment variables
    payment = None
    total_price = 0

    # Check if payment is for device cart or medicine cart
    if cart_type == "device":
        cart = Divicecart.objects.filter(user=user)
        total_price = sum(i.quantity * i.device.price for i in cart)
    elif cart_type == "medicine":
        cart = Medcart.objects.filter(user=user)
        total_price = sum(item.subtotal() for item in cart)
    else:
        messages.error(request, "Invalid cart type selected.")
        return redirect("cart_view")

    # Debugging
    print(f"Cart Type: {cart_type}, Total Price: {total_price}")

    if total_price == 0:
        messages.error(request, f"Your {cart_type} cart is empty.")
        return redirect("cart_view" if cart_type == "device" else "med_cart_view")

    # Create a payment order for the selected cart
    try:
        payment = client.order.create({
            "amount": int(total_price * 100),  # Razorpay accepts amount in paise
            "currency": order_currency,
            "payment_capture": "1",
        })
    except Exception as e:
        messages.error(request, f"Payment Error: {e}")
        return redirect("cart_view" if cart_type == "device" else "med_cart_view")

    return render(
        request,
        "cart/Payment.html",
        {
            "razorpay_key": "rzp_test_W3mMQR6ikpp5sy",
            "payment": payment,
            "total": total_price,
            "cart_type": cart_type,  # Pass cart type to the template
        },
    )


logger = logging.getLogger(__name__)

def payment_success(request):
    """Handles post-payment logic after confirming payment."""
    payment_id = request.GET.get("payment_id")

    if not payment_id:
        messages.error(request, "Payment verification failed! Please contact support.")
        return redirect("customerpanel")

    user = request.user
    customer = Customer.objects.filter(user=user).first()  # Get associated customer details
    device_cart_items = Divicecart.objects.filter(user=user)
    med_cart_items = Medcart.objects.filter(user=user)

    if not device_cart_items.exists() and not med_cart_items.exists():
        messages.error(request, "No items in cart to process.")
        return redirect("customerpanel")

    order_items = []
    total_price = 0

    try:
        with transaction.atomic():
            # Process device orders
            for item in device_cart_items:
                device = get_object_or_404(DeviceInformation, id=item.device.id)

                logger.info(f"Before: {device.product_name} stock = {device.quantity_available}")

                if device.quantity_available < item.quantity:
                    messages.error(request, f"Not enough stock for {device.product_name}.")
                    return redirect("cart_view")

                device.quantity_available -= item.quantity
                device.save()

                logger.info(f"After: {device.product_name} stock = {device.quantity_available}")

                order_items.append({
                    "Productname": device.product_name,
                    "Quantity": item.quantity,
                    "Total_Price": item.subtotal(),
                })
                total_price += item.subtotal()

            # Process medicine orders
            for item in med_cart_items:
                medicine = get_object_or_404(Medicine_inventory, id=item.medicine.id)

                logger.info(f"Before: {medicine.medicine_name} stock = {medicine.quanity_availble}")

                if medicine.quanity_availble < item.quantity:
                    messages.error(request, f"Not enough stock for {medicine.medicine_name}.")
                    return redirect("med_cart_view")

                medicine.quanity_availble -= item.quantity
                medicine.save()

                logger.info(f"After: {medicine.medicine_name} stock = {medicine.quanity_availble}")

                order_items.append({
                    "Productname": medicine.medicine_name,
                    "Quantity": item.quantity,
                    "Total_Price": item.subtotal(),
                })
                total_price += item.subtotal()

            # Create an Order record
            order = Order.objects.create(
                user=user,
                device=device_cart_items.first().device if device_cart_items.exists() else None,
                medicine=med_cart_items.first().medicine if med_cart_items.exists() else None,
                total_price=total_price,
                no_of_items=len(order_items),
                order_status="Processing",
                delivary_status="Pending",
                address=customer.address if customer else "No Address Provided",
                phone=customer.phone if customer else None,
            )

            # Clear the cart after successful order placement
            device_cart_items.delete()
            med_cart_items.delete()

        messages.success(request, "Payment successful! Your order has been placed.")
        return render(request, "cart/payment_success.html", {"payment_id": payment_id, "order": order})

    except Exception as e:
        logger.error(f"Payment processing error: {str(e)}")
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("customerpanel")