from django.shortcuts import render, HttpResponse,get_object_or_404
from products.models import Category, Product
from .models import Post
import json
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def posts(request):
    posts = Post.objects.all()
    items_per_page = 3
    paginator = Paginator(posts, items_per_page)

    page = request.GET.get('page', 1)

    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        
        
    categories = Category.objects.filter(posts__isnull=False).distinct()
    return render(request, 'posts/posts.html', {
        'posts' : posts,
        'categories': categories,
        'current_page': current_page,
    })




def post_category(request, slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(category = category)
    categories = Category.objects.filter(posts__isnull=False).distinct()
    return render(request, 'posts/post_category.html', {
        'posts' : posts,
        'categories': categories,
        'category' : category,
    })


@login_required(login_url='login')
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        new_post = form.save(commit=False)
        new_post.auther = request.user
        new_post.save()
        return post_view(request, new_post.slug)
    else:
        post_form = PostForm()
        return render(request, 'posts/add_post.html', {
            'post_form':post_form,
            })
    
    
    
def post_view(request, slug):
    post = Post.objects.get(slug=slug)
    categories = Category.objects.filter(posts__isnull=False).distinct()
    return render(request, 'posts/post.html', {
        'post': post,
        'categories' : categories,
    })
    

@login_required(login_url='login') 
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
        

@login_required(login_url='login')
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        return posts(request)