from django.shortcuts import render
from product.models import Product
# Create your views here.
def home(request):
    
    products=Product.objects.all().filter(is_available=True)
    return render(request,'kartapp/home.html',{'products':products})
