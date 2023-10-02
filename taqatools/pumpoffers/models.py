from django.db import models
from django.contrib.auth.models import User
from members.models import Address, Company
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.


class Irrigation(models.Model):
    type = models.CharField(max_length=55)
    
    def __str__(self):
        return self.type
    
class PowerSource(models.Model):
    source = models.CharField(max_length=55)
    
    def __str__(self):
        return self.source
    
class Validity(models.Model):
    period = models.CharField(max_length=55)
    days = models.PositiveSmallIntegerField() 
    
    def __str__(self):
        return self.period 
    
class PumpOfferRequest(models.Model):
    user = models.ForeignKey(User, related_name='pumpoffer', on_delete=models.SET_NULL, null=True)
    hp = models.FloatField()
    gwdepth = models.PositiveIntegerField()
    boreholediam = models.PositiveIntegerField()
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    irrigation = models.ForeignKey(Irrigation, on_delete=models.SET_NULL, null=True)
    power = models.ForeignKey(PowerSource, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


class PumpOffer(models.Model):
    request = models.ForeignKey(PumpOfferRequest, on_delete=models.SET_NULL, null=True, related_name='offers')
    company  = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='offers')
    value = models.FloatField(default=0)
    valid = models.ForeignKey(Validity, on_delete=models.SET_NULL, null=True)
    include_taxes = models.BooleanField(default=False)
    include_trans = models.BooleanField(default=False)
    installment = models.BooleanField(default=False)
    submit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    
    
class PumpOfferItem(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, related_name='pumpoffer')
    offer = models.ForeignKey(PumpOffer, on_delete=models.CASCADE, related_name='items')
    q = models.FloatField()
    price = models.FloatField(default=0)
    @property
    def item_value(self):
        return float(self.price) * float(self.q)


@receiver(post_save, sender =  PumpOfferItem)
def update_details(sender, instance, created, **kwargs):
    if created:
        instance.offer.value += instance.item_value
        instance.offer.save()
    
@receiver(post_delete, sender =  PumpOfferItem)
def update_details(sender, instance,  **kwargs):
    instance.offer.value -= instance.item_value
    instance.offer.save()
    
