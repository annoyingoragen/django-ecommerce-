from .models import CartItem,Cart
from .views import _create_Cart
def counter(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart=Cart.objects.get(cart_id=_create_Cart(request))
            cartcount=cart.total_product_quantity
            print("total_product_quantity",cart.total_product_quantity)
            print("cartcount",cartcount)
            # cartcount=0
        except Cart.DoesNotExist:
            cartcount=0
        return dict(cartcount=cartcount)
