from django.urls import path
from . import views
urlpatterns=[
    path('',views.cart,name="cart"),
    path('add_cart/<int:product_id>',views.add_cartitem,name="add_to_cart"),
    path('reduce_cart/<int:product_id>/<int:cartitem_id>',views.reduce_cartitem,name="reduce_from_cart"),
    path("remove_cartitem/<int:cartitem_id>",views.remove_cartitem,name="remove_cartitem"),

    path('checkout',views.checkout,name='checkout'),
    ]