from math import prod
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from cart.models import Cart, CartItem
from product.models import Product,Variation



# Create your views here.

def cart(request):
    cart_items=0
    try:
        cart=Cart.objects.get(cart_id=_create_Cart(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        if cart_items.count()!=0:
            cart.total_amount=0
            cart.total_product_quantity=0
            for cart_item in cart_items:
            
                cart.total_amount+=(cart_item.sub_total())
                cart.total_product_quantity+=cart_item.quantity
            cart.save()
        else:
             cart_items=0

        
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_create_Cart(request)
        )
        cart.save()
    except CartItem.DoesNotExist:
         cart_items=[]
         print("sdj")

    return render(request,"cart/cart.html",{'cart':cart,'cart_item':cart_items})


def _create_Cart(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


def add_cartitem(request,product_id):
    product=Product.objects.get(id=product_id)
    product_variation=[]
    if request.method=='POST':
        for key in request.POST:
            if key=='csrfmiddlewaretoken':
                continue
            value=request.POST[key]
                
         
        
            var=Variation.objects.get(product=  product,variation_category=key,variation_value=value)

            product_variation.append(var)
  

    
    try:
        cart=Cart.objects.get(cart_id=_create_Cart(request))
        cart.save()
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_create_Cart(request)
        )
        cart.save()

    is_Cart_item_exists=CartItem.objects.filter(product=product,cart= cart  ).exists()
    if is_Cart_item_exists:
        cart_item=CartItem.objects.filter(product=product,cart= cart  )
        
        var_list=[]
        cart_item_ids=[]
        for item in cart_item:
            existing_variation=item.variations.all()
            var_list.append(list(existing_variation))
            cart_item_ids.append(item.id)

        if product_variation in var_list:
            index=var_list.index(product_variation)
            itemid=cart_item_ids[index]
            item=CartItem.objects.get(product=product,id=itemid)
            item.increase_quantity()
            item.save()
        else:
            cart_item=CartItem.objects.create(product=product,quantity=0,cart=cart)
            if len(product_variation)>0:
             for var in product_variation:
                        
                    cart_item.variations.add(var)

            cart_item.increase_quantity()
            cart_item.save()     
     
    else:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=0,
            cart=cart,
        )
        if len(product_variation)>0:
            for item in product_variation:
            
                cart_item.variations.add(item)
        cart_item.increase_quantity()
        cart_item.save()
    
    return redirect('cart')

def reduce_cartitem(request,product_id,cartitem_id):
    cart=Cart.objects.get(cart_id=_create_Cart(request))
    product=Product.objects.get(id=product_id)
    cartitem=CartItem.objects.get(product=product,cart=cart,id=cartitem_id)
    if cartitem.quantity>1:
        cartitem.decrease_quantity()
        cartitem.save()
    else:
        cartitem.delete()
    return redirect('cart')

def remove_cartitem(request,cartitem_id):
    cartitem=CartItem.objects.get(id=cartitem_id)
    cartitem.remove_quantity()
    cartitem.delete()
    return redirect('cart')