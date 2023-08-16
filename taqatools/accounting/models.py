from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Category

# Create your models here.


class PurchaseInvoice(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='purchase')
    created_at = models.DateTimeField(auto_now=True)
    value = models.FloatField()
    
    
class PurchaseInvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='purchase')
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField()
    
class SaleInvoice(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sale')
    created_at = models.DateTimeField(auto_now=True)
    value = models.FloatField()
    
    @property
    def total_value(self):
        return sum((item.price*item.q) for item in self.items.all() )
    
    
class SaleInvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='sale')
    invoice = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField()
    
class Credit(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='credit')
    created_at = models.DateTimeField(auto_now=True)
    value = models.FloatField()
    
    
class Depit(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='depit')
    created_at = models.DateTimeField(auto_now=True)
    value = models.FloatField()
    

class TermCondition(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='terms')
    
class Offer(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='offer')
    created_at = models.DateTimeField(auto_now=True)
    value = models.FloatField()
    
    
class OfferItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='offer')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField()
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='cart')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartitems')
    q = models.PositiveBigIntegerField(default=1)
    price = models.FloatField()