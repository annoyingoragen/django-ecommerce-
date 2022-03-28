from .models import CartItem,Cart
from .views import _create_Cart
from django.contrib.auth.decorators import login_required
def counter(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                cartcount=0
                cart_items=CartItem.objects.all().filter(user=request.user)
                for cart_item in cart_items:
                  cartcount+=cart_item.quantity  
            else:
                cart=Cart.objects.get(cart_id=_create_Cart(request))
                cartcount=cart.total_product_quantity
                print("total_product_quantity",cart.total_product_quantity)
                print("cartcount",cartcount)
            # cartcount=0
        except Cart.DoesNotExist:
            cartcount=0
        return dict(cartcount=cartcount)
