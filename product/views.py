from django.core import paginator
from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import category
from cart.models import CartItem,Cart
from cart.views import _create_Cart
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q

from django.http.response import HttpResponse

# Create your views here.
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
      paginator=Paginator(products,2)

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
        products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(description__icontains=keyword))
        product_count=products.count()
        return render(request,'product\store.html',{'products':products,'product_count':product_count})
  return render(request,'product\store.html')


def productdetail(request,category_slug,product_slug):
   try:
      product=Product.objects.get(category__slug=category_slug,slug=product_slug)
      cartitem=CartItem.objects.filter(cart__cart_id=_create_Cart(request),product=product).exists()
   except Exception as e:
      raise e
   print(product.variation_set)
   return render(request,'product\product_detail.html',{'product':product,'exist_in_cart':cartitem})