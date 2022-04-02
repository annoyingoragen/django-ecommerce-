from django.contrib import admin
from .models import Payment,Order,OrderDetail
# Register your models here.

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderDetail)



