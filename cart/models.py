from operator import mod
from re import T
from django.db import models
from django.db.models.fields.related import ForeignKey
from product.models import Product, Variation
# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250)
    date_added=models.DateField(auto_now_add=True)
    total_product_quantity=models.IntegerField(default=0, blank=True)
    total_amount=models.FloatField(default=0,blank=True)

    def __str__(self) -> str:
        return self.cart_id

class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation,blank=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    
    def increase_quantity(self):
        self.quantity+=1
        self.cart.total_product_quantity+=1
    
    def decrease_quantity(self):
        print(self.cart.total_product_quantity)
        self.quantity-=1
        self.cart.total_product_quantity-=1
        print('decreasing',self.cart.total_product_quantity)

    def remove_quantity(self):
            print(self.cart.total_product_quantity)
            self.cart.total_product_quantity=self.cart.total_product_quantity-self.quantity
            print('removing',self.cart.total_product_quantity)
            self.quantity=0

    def sub_total(self):
        return self.product.price * self.quantity
    def __unicode__(self):
        return self.product