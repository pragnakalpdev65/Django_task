from django.urls import path
from .views import (
    IndexView, PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts/', PostListView.as_view(), name='showblog'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
]





















# from django.urls import path
# from . import views

# urlpatterns = [
# path('', views.index, name='index'),
# path('posts/',views.showblog,name='showblog'),
# path('create/', views.create_post, name='create_post'),
# path('posts/<int:post_id>/', views.post_detail, name='post_detail'),  # new
# path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),  # ✅ new
# path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # ✅ new

# ]