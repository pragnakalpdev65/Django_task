from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, View, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Product, Category,Cart,Order,OrderItem,ShippingDetail
from .forms import ShippingForm
from django.db.models import Q


class IndexView(TemplateView):
    template_name = 'E_commerce_app/home.html'

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'E_commerce_app/registration.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Change your password or username")
            return render(request, 'E_commerce_app/registration.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'E_commerce_app/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('category_list')
        else:
            messages.error(request, "Invalid username or password!")
            return render(request, 'E_commerce_app/login.html', {'error': 'Invalid credentials'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('login')
        
class CategoryView(ListView):
    model = Category
    template_name = 'E_commerce_app/category.html'
    context_object_name = 'categories'
    # def category_list(request):
    #     categories = Category.objects.all()
    #     print(">>>>>>>>>",categories)
    #     return render(request, 'E_commerce_app/category.html', {'categories': categories})
    

class SearchView(ListView):
    model = Product
    template_name = 'E_commerce_app/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        return Product.objects.none() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class CategoryProductsView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        return render(request, 'E_commerce_app/product_by_category.html', {
            'category': category,
            'products': products
        })

class ProductDetailView(DetailView):
    model = Product
    template_name = 'E_commerce_app/product_detail.html'
    context_object_name = 'product'

class AddToCartView(View):
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            print("true")
            return redirect('login')

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}  
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('product_by_category',category_id=product.category.id) 


class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
        else:
            cart_items = []

        total = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'E_commerce_app/cart.html', {
            'cart_items': cart_items,
            'total': total
        })

class AddItemView(View):
    def post(self, request, cart_id):
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        cart_item.quantity += 1
        cart_item.save()

        messages.success(request, "Item added to cart!")
        return redirect('cart')

class RemoveItemView(View):
     def post(self, request, cart_id):
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.success(request, "Item remove from cart!")
        return redirect('cart')

class CreateOrderView(View):
  
    def get(self,request):

        cart_items = Cart.objects.filter(user=request.user)
        if cart_items.exists():
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            
            order = Order.objects.create(total_price=total_price, user = request.user)
            
            for item in cart_items:
                OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
                )
            request.session['order_id'] = order.id 
            return redirect('shippingdetail')
        return redirect('cart')

class OrderDetailView(DetailView):

    def get(self,request,order_id=None):
        cart_items = Cart.objects.filter(user=request.user)

        if order_id:
            order=get_object_or_404(Order,id=order_id,user=request.user)
            order_item = OrderItem.objects.filter(order=order)     
            total = sum(item.product.price * item.quantity for item in order_item)
            print(order)
            print(order_item)
            order_details = []
            for item in order_item:
                order_details.append({
                    "item_name": item.product.name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "total_price": item.price * item.quantity,
                })
            print(order_details)
            return render(request,'E_commerce_app/order_details.html',{
                'order':order,
                'order_items':order_details,
                'total':total,
            })   

        else:
            orders = Order.objects.filter(user=request.user)
            return render(request, 'E_commerce_app/order_list.html', {
                'orders': orders
            })

class ShippingDetailView(View):
    template_name = 'E_commerce_app/shipping_detail.html'
    

    def get(self, request):
        form = ShippingForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        name = request.POST.get('name')
        address = request.POST.get('address')
        mail = request.POST.get('mail')

        ShippingDetail.objects.create(name=name, address=address, mail=mail)
        cart_items.delete()
        return redirect('thanks')
    
class ThanksView(TemplateView):
    template_name = 'E_commerce_app/thanks.html'
    def get(self, request):
        print(request.session.get("order_id"))
        return render(request, self.template_name)

