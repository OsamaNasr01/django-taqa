from django.db import models


# Create your models here.

class Site(models.Model):
    users = models.PositiveIntegerField(default=0)
    companies = models.PositiveIntegerField(default=0)
    categories = models.PositiveIntegerField(default=0)
    products = models.PositiveIntegerField(default=0)
    brands = models.PositiveIntegerField(default=0)
    sales = models.PositiveIntegerField(default=0)
    offers = models.PositiveIntegerField(default=0)
    pageview = models.PositiveIntegerField(default=0)