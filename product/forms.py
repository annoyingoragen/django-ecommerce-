from pyexpat import model
from django import forms
from .models import ReviewRating
class Reviewform(forms.ModelForm):
    class Meta:
        model=ReviewRating

        fields=['subject','reviewtext','rating']
