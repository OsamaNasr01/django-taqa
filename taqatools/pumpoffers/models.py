from django.db import models
from django.contrib.auth.models import User
from members.models import Address, Company

# Create your models here.

class PumpOfferRequest(models.Model):
    user = models.ForeignKey(User, related_name='pumpoffer', on_delete=models.SET_NULL, null=True)
    hp = models.FloatField()
    gwdepth = models.PositiveIntegerField()
    boreholediam = models.PositiveIntegerField()
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PumpOffer(models.Model):
    request = models.ForeignKey(PumpOfferRequest, on_delete=models.SET_NULL, null=True, related_name='offers')
    company  = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='offers')
    value = models.FloatField(default=0)
    submit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    
    
class PumpOfferItem(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, related_name='pumpoffer')
    offer = models.ForeignKey(PumpOffer, on_delete=models.CASCADE, related_name='items')
    q = models.PositiveSmallIntegerField()
    price = models.FloatField(default=0)
    @property
    def item_value(self):
        return self.price * self.q

    