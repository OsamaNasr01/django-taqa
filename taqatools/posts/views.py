from django.shortcuts import render, HttpResponse
from products.models import Category
from .models import Post
import json

# Create your views here.
def posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/posts.html', {
        'posts' : posts,
    })



def add_post(request):
    if request.method == 'POST':
        print('post')
        data = json.loads(request.body)
        print(data)
        new_post = Post.objects.create(
            title = data['title'],
            content = data['content'],
            auther = request.user,
            category = Category.objects.get(id=data['category']) 
        )
        new_post.save
        json_data = json.dumps({'messege':'The post is submitted successfully'})
        return HttpResponse(json_data, content_type="application/json")
    else:
        categories  = Category.objects.all()
        return render(request, 'posts/add_post.html', {'categories': categories})
    
    
    
def post_view(request, slug):
    post = Post.objects.get(slug=slug)
    category_posts = Post.objects.filter(category = post.category).exclude(id= post.id)
    return render(request, 'posts/post.html', {
        'post': post,
        'category_posts': category_posts,
    })