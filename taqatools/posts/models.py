from django.db import models
from django.contrib.auth.models import User
from products.models import Category

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=150)
    



class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    auther = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title