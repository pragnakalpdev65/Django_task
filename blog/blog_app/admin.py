from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'post_date')  
    list_filter = ('post_date',)                
    search_fields = ('title', 'content')        
    ordering = ('-post_date',)               

admin.site.register(Post, PostAdmin)
