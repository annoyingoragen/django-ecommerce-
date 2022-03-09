from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number','password']

    def clean(self):
        cleaned_Data=super(RegistrationForm,self).clean()
        password=cleaned_Data.get('password')
        confirm_password=cleaned_Data.get('confirm_password')

        if password!=confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

  
    