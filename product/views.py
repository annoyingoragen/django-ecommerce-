from email import message
from urllib import request
from django.shortcuts import render ,redirect
from django.core import paginator
from django.shortcuts import redirect, render,get_object_or_404
from .models import Product,ReviewRating,ProductGallery
from category.models import category
from cart.models import CartItem,Cart
from cart.views import _create_Cart
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from .forms import Reviewform
from order.models import OrderDetail
from django.contrib import messages
from django.http.response import HttpResponse

# Create your views here.
def submit_review(request,product_id):
  print("in ere")
  url=request.META.get('HTTP_REFERER')
  if request.method=='POST':
    print("posy")
    try:
      review= ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
      form=Reviewform(request.POST,instance=review)
      form.save()
      messages.success(request,'Your review has been updated')
      return redirect(url)
    except ReviewRating.DoesNotExist:
      form=Reviewform(request.POST)
      if form.is_valid():
        print("in form")
        reviewdata=ReviewRating()
        reviewdata.subject=form.cleaned_data['subject']
        reviewdata.rating=form.cleaned_data['rating']
        reviewdata.reviewtext=form.cleaned_data['reviewtext']
        reviewdata.ip=request.META.get('REMOTE_ADDR')
        reviewdata.product=Product.objects.get(id=product_id)
        reviewdata.user=request.user
        reviewdata.save( )
        messages.success(request,'Your review has been submitted')
        return redirect(url)



      



def store(request,category_slug=None):
   categories=None
   products=None
   if category_slug !=None:
      categories=get_object_or_404(category,slug=category_slug)
      products=Product.objects.filter(category=categories,is_available=True)
     
      page=request.GET.get('page',1)
      paginator=Paginator(products,1)
      
      try:
        paged_products=paginator.get_page(page)
      except PageNotAnInteger:
        paged_products = paginator.page(1)
      except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)
      
      product_count=products.count()
   else:
      products=Product.objects.all().filter(is_available=True)
      page=request.GET.get('page')
      paginator=Paginator(products,4)

      try:
        paged_products=paginator.get_page(page)
      except PageNotAnInteger:
        paged_products = paginator.page(1)
      except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)
      
      product_count=products.count()
   return render(request,'product\store.html',{'products':paged_products,'product_count':product_count})


def search(request):
  if 'keyword' in request.GET:
      keyword=request.GET['keyword']
      if keyword:
        products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword)|Q(description__icontains=keyword))
        product_count=products.count()
        return render(request,'product\store.html',{'products':products,'product_count':product_count})
  return render(request,'product\store.html')




def productdetail(request,category_slug,product_slug):
   try:
      product=Product.objects.get(category__slug=category_slug,slug=product_slug)
      cartitem=CartItem.objects.filter(cart__cart_id=_create_Cart(request),product=product).exists()
   except Exception as e:
      raise e
   if request.user.is_authenticated:
     try:
       orderedproduct=OrderDetail.objects.filter(user=request.user,product_id=product.id).exists()
     except OrderDetail.DoesNotExist:
       orderedproduct=None 
   else:
      orderedproduct=None
   
   reviews=ReviewRating.objects.filter(product=product,status=True)
   productgallery=ProductGallery.objects.filter(product_id=product.id)
   return render(request,'product\product_detail.html',{'product':product,'productgallery':productgallery,'orderedproduct':orderedproduct,'exist_in_cart':cartitem,'reviews':reviews})