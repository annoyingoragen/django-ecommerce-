from operator import mod
from pyexpat import model
from re import search
from django.contrib import admin
from .models import Payment,Order,OrderDetail
# Register your models here.

class DetailsOfOrder(admin.TabularInline):
    model=OrderDetail
    extra=0
    readonly_fields=('Payment','user','product','quantity','product_price','order','variation')


class OrderAdmin(admin.ModelAdmin):
    list_display=['full_name','created_at','order_number','status','email','is_ordered']
    list_filter=['status','is_ordered']
    search_fields=["order_number",'first_name','last_name','phone']
    list_per_page=20
    inlines=[DetailsOfOrder]

class OrderDetailAdmin(admin.ModelAdmin):
    readonly_fields=('Payment','user','product','quantity','product_price','order','variation')

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetail,OrderDetailAdmin)



