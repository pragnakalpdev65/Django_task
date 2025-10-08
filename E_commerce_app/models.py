# xg6KHa4GPzQqqS@-pass for h
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
  name=models.CharField(max_length=500)

  def __str__(self):
    return self.name

class Product(models.Model):
  name=models.CharField(max_length=500)
  description=models.TextField()
  price=models.PositiveIntegerField()
  image=models.ImageField(upload_to='product_images/')
  category=models.name = models.ForeignKey('Category',on_delete=models.CASCADE)

  def __str__(self):
      return self.name
      

class CartItem(models.Model):
  product = models.ForeignKey('Product', on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField()

  def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Order(models.Model):
    item = models.CharField(max_length=500)
    total_price=models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"
    
