from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import category


# Create your views here.
def store(request,category_slug=None):
   categories=None
   products=None
   if category_slug !=None:
      categories=get_object_or_404(category,slug=category_slug)
      products=Product.objects.filter(category=categories,is_available=True)
      product_count=products.count()
   else:
      products=Product.objects.all().filter(is_available=True)
      product_count=products.count()
   return render(request,'product\store.html',{'products':products,'product_count':product_count})



def productdetail(request,category_slug,product_slug):
   try:
      product=Product.objects.get(category__slug=category_slug,slug=product_slug)
   except Exception as e:
      raise e

   return render(request,'product\product_detail.html',{'product':product})