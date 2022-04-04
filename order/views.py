from calendar import month
from datetime import datetime

from django.shortcuts import redirect, render
from cart.models import CartItem
from product.models import Product 
from .forms import Orderform
from .models import Order,OrderDetail,Payment
from product.models import Product


import datetime
import json
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.
def payment(request):
    body=json.loads(request.body)
    print(body)
    #saving transaction details inside payment model and order model
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

    # after transaction is done copy items from cart into order history
    cart_items=CartItem.objects.filter(user=request.user )

    for item in cart_items:
        orderdetail=OrderDetail()
        orderdetail.order=order
        orderdetail.Payment=payment
        orderdetail.user=request.user
        orderdetail.product=item.product
        orderdetail.quantity=item.quantity
        orderdetail.product_price=item.product.price
        orderdetail.ordered=True
        orderdetail.save()
        cart_item=CartItem.objects.get(id=item.id)
        product_variation=cart_item.variations.all()
        orderdetail=OrderDetail.objects.get(id=orderdetail.id)
        orderdetail.variation.set(product_variation)
        orderdetail.save()


    #reduce the product quantity

        product=Product.objects.get(id=item.product_id)
        product.stock-=item.quantity   
        product.save()


    #clear cart

    CartItem.objects.filter(user=request.user).delete()

    #send email to customer about order
    mail_subject="Thank you for ordering"
    message=render_to_string('order/order_recieved_email.html',{
                'user':request.user,
                'order':order
                })
    to_email=request.user.email
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()

    # redirect user  to thank you page by sending data back to Payment Page through json
    order_complete_data={
        'order_number':body['orderID'],
        'transactionID': body['transactionID'],

    }
    return JsonResponse( order_complete_data)



    # return render(request,'order/payment.html')


def order_complete(request):
    order_number= request.GET.get('order_number')
    transactionID=request.GET.get('payment_id')
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products=OrderDetail.objects.filter(order_id=order.id)
        subtotal =0
        for i in ordered_products:
            subtotal +=i.product_price*i.quantity
            
        return render(request,"order/order_complete.html",{'order_number':order_number,'transactionID':transactionID,'order':order,'ordered_products':ordered_products,'subtotal':subtotal})
    except(Order.DoesNotExist):
        return redirect('Home')

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