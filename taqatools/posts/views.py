from django.shortcuts import render, HttpResponse
from products.models import Category
from .models import Post
import json

# Create your views here.
def posts(request):
    return render(request, 'posts/posts.html', {})



def add_post(request):
    if request.method == 'POST':
        print('post')
        data = json.loads(request.body)
        print(data)
        new_post = Post.objects.create(
            title = data['title'],
            content = data['content'],
            category = data['category']
        )
        new_post.save
        json_data = json.dumps({'ok':'ok'})
        return HttpResponse(json_data, content_type="application/json")
    else:
        categories  = Category.objects.all()
        return render(request, 'posts/add_post.html', {'categories': categories})