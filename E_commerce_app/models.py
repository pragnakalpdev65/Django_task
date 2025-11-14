# xg6KHa4GPzQqqS@-pass for h
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
  name=models.CharField(max_length=500)
  image = models.ImageField(upload_to='category_images/', blank=True, null=True)


  def __str__(self):
    return self.name

class Product(models.Model):
  name=models.CharField(max_length=500)
  description=models.TextField()
  price=models.PositiveIntegerField()
  image=models.ImageField(upload_to='product_images/')
  category=models.ForeignKey('Category',on_delete=models.CASCADE)

  def __str__(self):
      return self.name
      

class Cart(models.Model):
  product = models.ForeignKey('Product', on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Added user


  def __str__(self):
        return f"{self.product.name} x {self.quantity}"

  def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total_price=models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

class ShippingDetail(models.Model):
    name=models.CharField( max_length=50)
    address=models.TextField()
    mail=models.EmailField(max_length=254)