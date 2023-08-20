from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Category
from sitestats.models import Site
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.


class PurchaseInvoice(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='purchase')
    created_at = models.DateTimeField(auto_now=True)
    @property
    def total_value(self):
        return sum((item.item_value) for item in self.items.all() )
    
@receiver(post_save, sender =  PurchaseInvoice)
def update_details(sender, instance, created, **kwargs):
    if created:
        instance.user.account.details.purchases_no += 1
        instance.user.account.details.save()
    
@receiver(post_delete, sender =  PurchaseInvoice)
def update_details(sender, instance,  **kwargs):
    instance.user.account.details.purchases_no -= 1
    instance.user.account.details.save()
    
    
    
class PurchaseInvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='purchase')
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField(default=0)
    @property
    def item_value(self):
        return self.price * self.q
    
@receiver(post_save, sender =  PurchaseInvoiceItem)
def update_details(sender, instance, created, **kwargs):
    if created:
        instance.invoice.user.account.details.purchases_value += instance.item_value
        instance.invoice.user.account.details.save()
    
@receiver(post_delete, sender =  PurchaseInvoiceItem)
def update_details(sender, instance,  **kwargs):
    instance.invoice.user.account.details.purchases_value -= instance.item_value
    instance.invoice.user.account.details.save()

    
class SaleInvoice(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sale')
    created_at = models.DateTimeField(auto_now=True)
    count = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default=1)
    @property
    def total_value(self):
        return sum((item.item_value) for item in self.items.all() )
    
@receiver(post_save, sender =  SaleInvoice)
def update_details(sender, instance, created, **kwargs):
    if created:
        print(instance.user)
        instance.user.account.details.sales_no += 1
        instance.user.account.details.save()
    
@receiver(post_delete, sender =  SaleInvoice)
def update_details(sender, instance,  **kwargs):
    print(instance.user)
    instance.user.account.details.sales_no -= 1
    instance.user.account.details.save()
    
    
    
    
class SaleInvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='sale')
    invoice = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price =models.FloatField(default=0)
    @property
    def item_value(self):
        return self.price * self.q
    
@receiver(post_save, sender =  SaleInvoiceItem)
def update_details(sender, instance, created, **kwargs):
    if created:
        instance.invoice.user.account.details.sales_value += instance.item_value
        instance.invoice.user.account.details.save()
    
@receiver(post_delete, sender =  SaleInvoiceItem)
def update_details(sender, instance,  **kwargs):
    instance.invoice.user.account.details.sales_value -= instance.item_value
    instance.invoice.user.account.details.save()

    
class Credit(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='credit')
    created_at = models.DateTimeField(auto_now=True)
    value = models.FloatField(default=0)
    
@receiver(post_save, sender =  Credit)
def update_details(sender, instance, created, **kwargs):
    if created:
        instance.user.account.details.payments_no += 1
        instance.user.account.details.payments_value += float(instance.value)
        instance.user.account.details.save()
    
@receiver(post_delete, sender =  Credit)
def update_details(sender, instance,  **kwargs):
    instance.user.account.details.payments_no -= 1
    instance.user.account.details.payments_value -= float(instance.value)
    instance.user.account.details.save()

    
class Depit(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='depit')
    created_at = models.DateTimeField(auto_now=True)
    value = models.FloatField(default=0)
    
@receiver(post_save, sender =  Depit)
def update_details(sender, instance, created, **kwargs):
    if created:
        print(instance.user)
        instance.user.account.details.receipts_no += 1
        instance.user.account.details.receipts_value += float(instance.value)
        instance.user.account.details.save()
    
@receiver(post_delete, sender =  Depit)
def update_details(sender, instance, **kwargs):
    instance.user.account.details.receipts_no -= 1
    instance.user.account.details.receipts_value -= float(instance.value)
    instance.user.account.details.save()


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
        return sum((item.item_value) for item in self.items.all() )
    
@receiver(post_save, sender =  Offer)
def update_details(sender, instance, created, **kwargs):
    if created:
        instance.user.account.details.offers_no += 1
        instance.user.account.details.save()
    
@receiver(post_delete, sender =  Offer)
def update_details(sender, instance, **kwargs):
    instance.user.account.details.offers_no -= 1
    instance.user.account.details.save()
    
class OfferItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='offer')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField(default=0)
    @property
    def item_value(self):
        return self.price * self.q
    
    
@receiver(post_save, sender =  OfferItem)
def update_details(sender, instance, created, **kwargs):
    if created:
        instance.offer.user.account.details.offers_value += instance.item_value
        instance.offer.user.account.details.save()
    
@receiver(post_delete, sender =  OfferItem)
def update_details(sender, instance,  **kwargs):
    instance.offer.user.account.details.offers_value -= instance.item_value
    instance.offer.user.account.details.save()

        
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='cart')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartitems')
    q = models.PositiveBigIntegerField(default=1)
    price = models.FloatField(default=0)
    @property
    def item_value(self):
        return self.price * self.q
    
