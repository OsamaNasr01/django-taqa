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
        new_post = Post.objects.create(
            title = request.POST.get('title'),
            content = request.POST.get('content'),
            auther = request.user,
            category = Category.objects.get(id=request.POST.get('category')) 
        )
        new_post.save
        json_data = json.dumps({'messege':'The post is submitted successfully'})
        return HttpResponse(json_data, content_type="application/json")
    else:
        post_form = PostForm()
        categories  = Category.objects.all()
        return render(request, 'posts/add_post.html', {
            'categories': categories,
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