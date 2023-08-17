from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Category
from sitestats.models import Site

# Create your models here.


class PurchaseInvoice(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='purchase')
    created_at = models.DateTimeField(auto_now=True)
    @property
    def total_value(self):
        return sum((item.price*item.q) for item in self.items.all() )
    
    
class PurchaseInvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='purchase')
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField()
    @property
    def item_value(self):
        return self.price * self.q
    
    
class SaleInvoice(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sale')
    created_at = models.DateTimeField(auto_now=True)
    count = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default=1)
    @property
    def total_value(self):
        return sum((item.price*item.q) for item in self.items.all() )
    def save(self, *args, **kwargs):
        super(SaleInvoice, self).save(*args, **kwargs)
        self.count.sales += 1
        self.count.save()
    
    
class SaleInvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='sale')
    invoice = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField()
    @property
    def item_value(self):
        return self.price * self.q
    
    
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
    count = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default=1)
    @property
    def total_value(self):
        return sum((item.price*item.q) for item in self.items.all() )
    def save(self, *args, **kwargs):
        super(Offer, self).save(*args, **kwargs)
        self.count.offers += 1
        self.count.save()
    
    
class OfferItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='offer')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField()
    @property
    def item_value(self):
        return self.price * self.q
    
        
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='cart')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartitems')
    q = models.PositiveBigIntegerField(default=1)
    price = models.FloatField()
    @property
    def item_value(self):
        return self.price * self.q
    
