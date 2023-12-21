from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.text import slugify
from sitestats.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField



def arabic_to_english_slug(text):
    # Define a dictionary that maps Arabic characters to their corresponding English characters
    arabic_to_english_map = {
        'ا': 'a',
        'أ': 'a',
        'إ': 'e',
        'ب': 'b',
        'ت': 't',
        'ث': 'th',
        'ج': 'j',
        'ح': 'h',
        'خ': 'kh',
        'د': 'd',
        'ذ': 'th',
        'ر': 'r',
        'ز': 'z',
        'س': 's',
        'ش': 'sh',
        'ص': 's',
        'ض': 'dh',
        'ط': 't',
        'ظ': 'dth',
        'ع': '3',
        'غ': 'gh',
        'ف': 'f',
        'ق': 'q',
        'ك': 'k',
        'ل': 'l',
        'م': 'm',
        'ن': 'n',
        'ه': 'h',
        'و': 'w',
        'ي': 'y',
        'ئ': 'e',
        'ء': 'a',
        'ؤ': 'o',
        'ة': 'h',
        'ى': 'a',
        # Add more mappings here
    }
    # Create a new string that replaces the Arabic characters with their corresponding English characters
    english_text = ''.join([arabic_to_english_map.get(char, char) for char in text])
    # Use the Django slugify function to generate the slug from the English text
    slug = slugify(english_text)
    return slug




class Gov(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class City(models.Model):
    name = models.CharField(max_length=100)
    gov = models.ForeignKey(Gov, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name
    
class Address(models.Model):
    details = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self):
        return self.details
    
    @property
    def location(self):
        return f'{self.city.gov.name}، {self.city.name}، {self.details}'



class CoCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    slug = models.SlugField(max_length=150, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.slug:
            self.slug = arabic_to_english_slug(self.name)
        super(CoCategory, self).save(*args, **kwargs)

class Company(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(max_length=200, null = True)
    address = models.ForeignKey(Address, on_delete = models.CASCADE, related_name = 'company')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company')
    category = models.ManyToManyField(CoCategory, related_name='companies', null= True)
    slug = models.SlugField(max_length=150, blank=True)
    count = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default=1)
    image = ResizedImageField(size=[300, 300], upload_to='images', null= True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.slug:
            self.slug = arabic_to_english_slug(self.name)
        super(Company, self).save(*args, **kwargs)
        self.count.companies += 1
        self.count.save()

def balance(self):
    sales = sum(invoice.total_value for invoice in self.sale.all())
    purchases = sum(invoice.total_value for invoice in self.purchase.all())
    payments = sum(payment.value for payment in self.credit.all())
    receipts = sum(receipt.value for receipt in self.depit.all())
    return -sales+purchases-payments+receipts

User.add_to_class('balance', balance)

def full_name(self):
    return f'{self.first_name} {self.last_name}'

User.add_to_class('full_name', full_name)

@receiver(post_save, sender=User)
def user_account_details(sender, instance, created, **kwargs):
    if created:
        details = Details.objects.create()
        Account.objects.create(user=instance, details= details)
        if not Site.objects.get(id=1):
            Site.objects.create()
        users_no =Site.objects.get(id=1)
        users_no.users   += 1
        users_no.save()
        
def has_company(self):
    return self.company.count()

User.add_to_class('has_company', has_company)



class Details(models.Model):
    sales_no = models.PositiveSmallIntegerField(default=0)
    sales_value = models.FloatField(default=0)
    purchases_no = models.PositiveSmallIntegerField(default=0)
    purchases_value = models.FloatField(default=0)
    offers_no = models.PositiveSmallIntegerField(default=0)
    offers_value = models.FloatField(default=0)
    payments_no = models.PositiveSmallIntegerField(default=0)
    payments_value = models.FloatField(default=0)
    receipts_no = models.PositiveSmallIntegerField(default=0)
    receipts_value = models.FloatField(default=0)
    
        

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.OneToOneField(Details, on_delete=models.CASCADE)
    image = ResizedImageField(size=[300, 300], upload_to='images', null= True, blank=True)
    @property
    def member(self):
        return self.user
    
    