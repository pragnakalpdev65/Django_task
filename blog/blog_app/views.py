from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm


class IndexView(TemplateView):
    template_name = 'blog_app/index.html'

class PostListView(ListView):
    model = Post
    template_name = 'blog_app/details.html'
    context_object_name = 'posts'
    ordering = ['post_date'] 

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_app/create_post.html'

    def get_success_url(self):
        return reverse('showblog')  

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_app/edit_post.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.id})

class PostDeleteView(DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = reverse_lazy('showblog')   
