from django import froms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class UserCreationForm(UserCreationForm):
    email=forms.forms.EmailField(required=True)

    class Meta:
        model=UserRegistration
        fields=("username","email","password1","password2")
