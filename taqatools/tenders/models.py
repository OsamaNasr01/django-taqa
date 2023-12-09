from django.db import models
from products.models import Category
from django.contrib.auth.models import User
from members.models import Address, Company

# Create your models here.



class Tender(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    
    
class Question(models.Model):
    text = models.CharField(max_length=155)
    type = models.IntegerField(choices=[
        (1, 'Numeric'),
        (2, 'Text'),
        (3, 'Boolean'),
    ])
    unit = models.CharField(max_length=50, null=True, blank=True)
    tender = models.ForeignKey(Tender, related_name='questions', on_delete=models.CASCADE)
    
    
    
class Choice(models.Model):
    text = models.CharField(max_length=55)
    Question  = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    
class TenderCategory(models.Model):
    category = models.ForeignKey(Category, related_name='tenders', on_delete=models.CASCADE)
    tender = models.ForeignKey(Tender, related_name='categories', on_delete=models.CASCADE)
    
class TenderRequest(models.Model):
    tender = models.ForeignKey(Tender, related_name='requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='tender_requests', on_delete=models.CASCADE)
    location = models.ForeignKey(Address, related_name='tenders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_created=True)
    
    
    
class Answer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    request = models.ForeignKey(TenderRequest, related_name='answers', on_delete=models.CASCADE)
    