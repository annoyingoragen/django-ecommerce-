from django.db import models

from category.models import category
from category.models import category
# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=75)
    slug=models.SlugField(max_length=80,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.FloatField()
    images=models.ImageField(upload_to="photos/products")
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product_name