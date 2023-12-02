
from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('posts/add-post/', views.add_post, name='add_post'),
    path('post/<slug:slug>/', views.post_view, name='post'),
    path('post/category/<slug:slug>/', views.post_category, name='post_category'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
]