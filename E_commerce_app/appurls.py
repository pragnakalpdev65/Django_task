from django.urls import path
from .views import IndexView, RegisterView, LoginView, CategoryView, CategoryProductsView, AddToCartView, CartView, AddItemView, RemoveItemView, OrderDetailView, CreateOrderView, ShippingDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('categories/', CategoryView.as_view(), name='category_list'),
    path('categories/<int:category_id>/', CategoryProductsView.as_view(), name='product_by_category'),
    path('addtocart/<int:product_id>/',AddToCartView.as_view(),name='add_to_cart'),
    path('cart/',CartView.as_view(),name='cart'),
    path('additem/<int:cart_id>',AddItemView.as_view(),name='additem'),
    path('removeitem/<int:cart_id>',RemoveItemView.as_view(),name='removeitem'),
    path('createorder/', CreateOrderView.as_view(), name='create_order'),
    path('orderdetail/', OrderDetailView.as_view(), name='order_list'),
    path('orderdetail/<int:order_id>/', OrderDetailView.as_view(), name='orderdetail'),
    path('shippingdetail/<int:shippindetail_id>/',ShippingDetailView.as_view(),name='shippingdetail'),
]
