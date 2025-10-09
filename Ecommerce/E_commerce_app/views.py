from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
 # Create your views here.
class IndexView(TemplateView):
    template_name='E_commerce_app/home.html'

class RegisterView(CreateView):
    model = User
    form_class=UserCreationForm
    template_name='E_commerce_app/registration.html'
    success_url=reverse_lazy('login')

class LoginView(LoginView):
    template_name='E_commerce_app/login.html'
    success_url=reverse_lazy('category')

# class CategoryView():
#     model=
#     templet_name='E_commerce_app/category.html'

# class ProductDetailView():
#     model=Product
#     template_name='E_commerce_app/product_detail.html'

# class ProductAddView():
#     model=Product
#     template_name='E_commerce_app/'

# class ProductRemoveView():
#     model=Product

# class CartView():
#     model=Product
#     template_name='E_commrce_app/cart.html'

# class UpdateCartView():
#     model=Product

# class AddresseView():

