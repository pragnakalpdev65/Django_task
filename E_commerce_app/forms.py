from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import ShippingDetail

class UserCreationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=["username","email","password1","password2"]


class ShippingForm(forms.ModelForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=ShippingDetail
        fields=['name','address','email']

