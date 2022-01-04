from django.db import models

# Create your models here.
class category (models.Model):
    name=models.CharField(max_length=75,unique=True)
    slug=models.SlugField(unique=True)
    description=models.TextField(max_length=255,blank=True)
    image=models.ImageField(upload_to='photos/categories',blank=True)
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
    def __str__(self) -> str:
        return self.name