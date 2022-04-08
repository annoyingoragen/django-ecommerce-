from base64 import urlsafe_b64decode
from email.message import EmailMessage
import profile
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.template import context
from django.contrib import messages,auth
from account.models import Account, UserProfile
from cart.models import Cart,CartItem
from .forms import RegistrationForm,UserForm,UserProfileForm
from django.contrib.auth.decorators import login_required
import requests
#for email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from order.models import Order, OrderDetail
from cart.views import _create_Cart
# Create your views here.


def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username=email.split("@")[0]

            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            
            user.save()
            
            userprofile=UserProfile(user=user)
            userprofile.save()
            current_site=get_current_site(request)
            mail_subject="Account activation"
            message=render_to_string('account/email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'We have sent you a verification email!')
            form=RegistrationForm
            context={
                'form':form
            }
            return render(request,'account/register.html',context)

    else:
            form=RegistrationForm
    context={
                'form':form
            }
    return render(request,'account/register.html',context)

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try :
                cart=Cart.objects.get(cart_id=_create_Cart(request))
                is_Cart_item_exists=CartItem.objects.filter(cart= cart  ).exists()
                if is_Cart_item_exists:
                    cart_item=CartItem.objects.filter(cart= cart  )
                    product_variation=[]
                    for item in cart_item:
                        variation=item.variations.all()
                        product_variation.append(list(variation))

                    cart_item=CartItem.objects.filter(user=user  )
                        
                    var_list=[]
                    cart_item_ids=[]
                    for item in cart_item:
                            existing_variation=item.variations.all()
                            var_list.append(list(existing_variation))
                            cart_item_ids.append(item.id)

                    for pv in product_variation:
                        if pv in var_list:
                            index=var_list.index(pv)
                            itemid=cart_item_ids[index]
                            item=CartItem.objects.get(id=itemid)
                            item.user=user
                            item.increase_quantity()
                            item.save()
                        else:
                            cart_item=CartItem.objects.filter(cart=cart  )
                            for item in cart_item:
                                item.user=user
                                item.save()
              #  cart.save()
            except:
                pass
            auth.login(request,user)
            url=request.META.get('HTTP_REFERER')
            query=requests.utils.urlparse(url).query
            print(query)
            if query =='next=/cart/checkout':
                return redirect('checkout')
            else:
                return redirect('home')
        else:
            messages.error(request,"invalid credentials")
            return redirect('login')
    return render(request,'account/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out")
    return redirect('login')
    

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Your account is activated")
        return redirect('login')

    else:

        messages.error(request,"Invalid activation link")
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    userprofile=UserProfile.objects.get(user=request.user)
    orders=Order.objects.filter(user=request.user,is_ordered=True)
    return render(request,'account/dashboard.html',{'orders':orders,'userprofile':userprofile})

@login_required(login_url='login')
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    return render(request,"account/my_orders.html",{'orders':orders})

@login_required(login_url='login')
def my_order_detail(request,order_id):
    print(order_id)
    
    order=Order.objects.get(order_number=order_id)
    ordered_products=OrderDetail.objects.filter(order_id=order.id)
    subtotal=order.order_total-order.tax
    
    return render(request,'account/my_order_detail.html',{
        'order_detail':ordered_products,
        'order':order,
        'subtotal':subtotal
    })

@login_required(login_url='login')
def edit_profile(request):
    userprofile=get_object_or_404(UserProfile,user=request.user)
    if request.method=='POST':
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm (request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)
        

    return render(request,'account/edit_profile.html',{"user_form":user_form,'profile_form':profile_form,'userprofile':userprofile})

@login_required(login_url='login')
def changepassword(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_new_password']
        user=Account.objects.get(username__exact=request.user.username)
        if new_password==confirm_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password updated successfully')
                return redirect('changepassword')
            else:
                messages.error(request,'your current password didnt match with your old password')
                return redirect('changepassword')
        else:
            messages.error(request,'Password does not match')
            return redirect('changepassword')



    return render(request,'account/changepassword.html')

def forgotpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__iexact=email)

            
            current_site=get_current_site(request)
            mail_subject="Password Reset"
            message=render_to_string('account/forgotpasswordemail.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'We have sent you a verification email!')
            return render(request,'account/login.html')
        else:
            messages.error(request,'Account does not exist')
            return render(request,'account/forgotpassword.html')
    return render(request,'account/forgotpassword.html')


def resetpassword_token(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Enter your new password')
        return render (request,'account/resetpassword.html')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')

def resetpassword(request):
    if request.method=='POST':
        password=request.POST['password']
        uid=request.session.get('uid')

        user=Account.objects.get(pk=uid)
        user.set_password(password)
        user.save()
        messages.success(request,'password changed successfully')
        return redirect('login')
    return render(request,'account/resetpassword.html')