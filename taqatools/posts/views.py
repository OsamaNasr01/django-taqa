from django.shortcuts import render, HttpResponse,get_object_or_404
from products.models import Category
from .models import Post
import json
from .forms import PostForm

# Create your views here.
def posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/posts.html', {
        'posts' : posts,
    })



def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        new_post = form.save(commit=False)
        new_post.save()
        return post_view(request, new_post.slug)
    else:
        post_form = PostForm()
        return render(request, 'posts/add_post.html', {
            'post_form':post_form,
            })
    
    
    
def post_view(request, slug):
    post = Post.objects.get(slug=slug)
    category_posts = Post.objects.filter(category = post.category).exclude(id= post.id)
    return render(request, 'posts/post.html', {
        'post': post,
        'category_posts': category_posts,
    })
    
    
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return post_view(request, slug)
    else:
        post_form = PostForm(instance=post)
        return render(request, 'posts/post_edit.html', {
            'post_form':post_form,
            'post':post,
            })