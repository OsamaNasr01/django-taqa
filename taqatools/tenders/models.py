from django.db import models
from products.models import Category,Product
from django.contrib.auth.models import User
from members.models import Address, Company
from django_resized import ResizedImageField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.



class Tender(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    image = ResizedImageField(size=[300, 300], upload_to='images', null= True, blank=True)
    
    
class Question(models.Model):
    text = models.CharField(max_length=155)
    type = models.IntegerField(choices=[
        (1, 'رقمي'),
        (2, 'نصي'),
        (3, 'نعم او لا'),
    ])
    unit = models.CharField(max_length=50, null=True, blank=True)
    re_of = models.IntegerField(choices=[
        (1, 'طلب'),
        (2, 'عرض'),
    ], default = 1)
    tender = models.ForeignKey(Tender, related_name='questions', on_delete=models.CASCADE)
    
    
    
class Choice(models.Model):
    text = models.CharField(max_length=55)
    question  = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    
class TenderCategory(models.Model):
    category = models.ForeignKey(Category, related_name='tenders', on_delete=models.CASCADE)
    tender = models.ForeignKey(Tender, related_name='categories', on_delete=models.CASCADE)
    
class TenderRequest(models.Model):
    tender = models.ForeignKey(Tender, related_name='requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='tender_requests', on_delete=models.CASCADE)
    location = models.ForeignKey(Address, related_name='tenders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
class Answer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    request = models.ForeignKey(TenderRequest, related_name='answers', on_delete=models.CASCADE)
    
    
    
class TenderOffer(models.Model):
    request = models.ForeignKey(TenderRequest, on_delete=models.SET_NULL, null=True, related_name='offers')
    company  = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='tender_offers')
    value = models.FloatField(default=0)
    submit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Terms(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, related_name='terms', on_delete=models.CASCADE)
    offer = models.ForeignKey(TenderOffer, related_name='terms', on_delete=models.CASCADE)    

class OfferItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='tender_offers')
    offer = models.ForeignKey(TenderOffer, on_delete=models.CASCADE, related_name='items')
    qty = models.FloatField()
    price = models.FloatField(default=0)
    @property
    def item_value(self):
        return float(self.price) * float(self.qty)


@receiver(post_save, sender =  OfferItem)
def update_details(sender, instance, created, **kwargs):
    if created:
        instance.offer.value += instance.item_value
        instance.offer.save()
    
@receiver(post_delete, sender =  OfferItem )
def update_details(sender, instance,  **kwargs):
    instance.offer.value -= instance.item_value
    instance.offer.save()