from django.shortcuts import render, HttpResponse,get_object_or_404
from products.models import Category, Product
from .models import Post
import json
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from members.views import not_auth

# Create your views here.



def admin_company(user):
    return user.is_superuser or user.has_company()

def is_superuser(user):
    return  user.is_superuser



def has_company(user):
    return user.has_company()  




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
    return render(request, 'posts/post_category.html', {
        'posts' : posts,
        'categories': categories,
        'category' : category,
        'current_page': current_page,
    })


@login_required(login_url='login')
@user_passes_test(admin_company, login_url='not_auth')  
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        new_post = form.save(commit=False)
        new_post.auther = request.user
        new_post.save()
        messages.success(request, ('تم اضافة المقال بنجاح'))
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
@user_passes_test(admin_company, login_url='not_auth')  
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.auther or request.user.is_superuser:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, ('تم تعديل المقال بنجاح'))
                return post_view(request, slug)
            else:
                messages.error(request, ('حدث خطأ اثناء تعديل المقال '))
                return post_view(request, slug)
        else:
            post_form = PostForm(instance=post)
            return render(request, 'posts/post_edit.html', {
                'post_form':post_form,
                'post':post,
                })
    else:
        return not_auth(request)
        

@login_required(login_url='login')
@user_passes_test(admin_company, login_url='not_auth')  
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.auther or request.user.is_superuser:
        if request.method == 'POST':
            post.delete()
            messages.success(request, ('تم حذف المقال بنجاح'))
            return posts(request)
    else:
        return not_auth(request)