from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, View, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Product, Category,Cart,Order,OrderItem,ShippingDetail
from .forms import ShippingForm



class IndexView(TemplateView):
    template_name = 'E_commerce_app/home.html'


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'E_commerce_app/registration.html'
    success_url = reverse_lazy('login')



class LoginView(BaseLoginView):
    template_name = 'E_commerce_app/login.html'



class CategoryView(ListView):
    model = Category
    template_name = 'E_commerce_app/category.html'
    context_object_name = 'categories'
    # def category_list(request):
    #     categories = Category.objects.all()
    #     print(">>>>>>>>>",categories)
    #     return render(request, 'E_commerce_app/category.html', {'categories': categories})
    

class CategoryProductsView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        return render(request, 'E_commerce_app/product_by_category.html', {
            'category': category,
            'products': products
        })
 

class AddToCartView(View):
    def post(self, request, product_id):
        if not request.user.is_authenticated:
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
        return redirect('cart')



class RemoveItemView(View):
     def post(self, request, cart_id):
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
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

            cart_items.delete()
            return redirect('orderdetail', order_id=order.id)
        return redirect('cart')


class OrderDetailView(DetailView):

    def get(self,request,order_id=None):
        cart_items = Cart.objects.filter(user=request.user)

        if order_id:
            order=get_object_or_404(Order,id=order_id,user=request.user)
            order_item = OrderItem.objects.filter(order=order)
            total = sum(item.product.price * item.quantity for item in order_item)
            print(total)
            return render(request,'E_commerce_app/order_details.html',{
                'order':order,
                'order_item':order_item,
                'total':total,
            })

        else:
            orders = Order.objects.filter(user=request.user)
            return render(request, 'E_commerce_app/order_details.html', {
                'orders': orders
            })

class ShippingDetailView(DetailView):
    template_name = 'E_commerce_app/shippind_detail.html'

    def get(self, request):
        shipping, created = ShippingDetail.objects.get_or_create(user=request.user)
        form = ShippingForm(instance=shipping)
        return render(request, self.template_name, {'form': form})


