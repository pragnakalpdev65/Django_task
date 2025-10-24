from django.contrib import admin
from .models import Category,Product,Cart,Order

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price','category','image')
    search_fields=('name',)
    list_filter=('category',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

admin.site.register(Cart)
admin.site.register(Order)


