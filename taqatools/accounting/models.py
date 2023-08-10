from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.


class PurchaseInvoice(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='purchase')
    created_at = models.DateTimeField(auto_now=True)
    value = models.PositiveIntegerField()
    
    
class PurchaseInvoiceItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='purchase')
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField()
    
class SaleInvoice(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sale')
    created_at = models.DateTimeField(auto_now=True)
    value = models.PositiveIntegerField()
    
    
class SaleInvoiceItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='sale')
    invoice = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField()
    
class Credit(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='credit')
    created_at = models.DateTimeField(auto_now=True)
    value = models.PositiveIntegerField()
    
    
class Depit(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='depit')
    created_at = models.DateTimeField(auto_now=True)
    value = models.PositiveIntegerField()
    