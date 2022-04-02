from calendar import month
from datetime import datetime
import imp
from django.shortcuts import redirect, render
from cart.models import CartItem 
from .forms import Orderform
from .models import Order,OrderDetail,Payment
import datetime
import json
# Create your views here.
def payment(request):
    body=json.loads(request.body)
    print(body)
    payment=Payment(
        user=request.user,
        payment_id=body['transactionID'],
        payment_method='paypal',
        status=body['status'],
        amount_paid=body['amount_paid'],
    )
    payment.save()

    order=Order.objects.get(user=request.user,order_number=body['orderID'])
    order.Payment=payment
    order.is_ordered=True
    order.save()

    return render(request,'order/payment.html')

def place_order(request):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    if cart_items.count()==0:
        return redirect('home')

    grandtotal=0
    tax=0
    total=0
    for cartitem in cart_items:
        total += (cartitem.product.price * cartitem.quantity)
        quantity =+cartitem.quantity
    tax=round((5/total)*100)
    grandtotal=total+tax

    if request.method=='POST':
        form=Orderform(request.POST)
       
        
        if form.is_valid():
            orderdata=Order()
            orderdata.user=current_user
            orderdata.first_name=form.cleaned_data['first_name']
            orderdata.last_name=form.cleaned_data['last_name']
            orderdata.phone=form.cleaned_data['phone']
            orderdata.email=form.cleaned_data['email']
            orderdata.address_line1=form.cleaned_data['address_line1']
            orderdata.address_line2=form.cleaned_data['address_line2']
            orderdata.country=form.cleaned_data['country']
            orderdata.state=form.cleaned_data['state']
            orderdata.city=form.cleaned_data['city']
            orderdata.order_note=form.cleaned_data['order_note']
            orderdata.order_total=grandtotal
            orderdata.tax=tax
            orderdata.status='New'
            orderdata.ip=request.META.get('REMOTE_ADDR')
            orderdata.save()
            
            year=int(datetime.date.today().strftime('%Y'))
            date=int(datetime.date.today().strftime('%d'))
            month=int(datetime.date.today().strftime('%m'))
           
            current_date=str(year)
            current_date+=str(month)
            current_date+=str(date)
            
            order_number=current_date+str(orderdata.id)
            orderdata.order_number=order_number
            orderdata.save()


            
            print(grandtotal)
            return render(request,'order/payment.html',{'order':orderdata,'cart_item':cart_items,'grandtotal':grandtotal,'tax':tax,'total':total})
        else:
            return redirect('checkout')

    else:
        return redirect('checkout')