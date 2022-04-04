import email
from itertools import product
from tkinter import CASCADE
from django.db import models
from account.models import Account
from product.models import Product,Variation
# Create your models here.

class Payment(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    amount_paid=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Cancelled','Cancelled'),
        ('Shipped','Shipped'),
        ('Completed','Completed'),
        

    )

    user=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    Payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number=models.CharField(max_length=20)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address_line1=models.CharField(max_length=50)
    address_line2=models.CharField(max_length=50,blank=True)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    order_note=models.CharField(max_length=100,blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default=None)
    ip=models.CharField(max_length=20,blank=True)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def address(self):
        return f'{self.address_line1} {self.address_line2}'
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
        
    def __str__(self):
        return self.first_name

class OrderDetail(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE) 
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    Payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation=models.ManyToManyField(Variation,blank=True)
 
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name