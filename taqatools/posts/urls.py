
from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('posts/add-post', views.add_post, name='add_post'),
    path('post/<slug:slug>', views.post_view, name='post')
]