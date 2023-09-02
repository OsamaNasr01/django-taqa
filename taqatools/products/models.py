from django.db import models
from django.utils.text import slugify
from sitestats.models import Site
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_resized import ResizedImageField

# Create your models here.

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

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    parent_id = models.PositiveIntegerField(null=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    count = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.slug:
            self.slug = arabic_to_english_slug(self.name)
        super(Category, self).save(*args, **kwargs)
    #     self.count.categories += 1
    #     self.count.save()
        
    
    # def delete(self, *args, **kwargs):
    #     super(Product, self).save(*args, **kwargs)
    #     self.count.categories -= 1
    #     self.count.save()
    
    
@receiver(post_save, sender =  Category)
def update_details(sender, instance, created, **kwargs):
    if created:
        site = Site.objects.get(id=1)
        site.categories +=1
        site.save()
    
@receiver(post_delete, sender =  Category)
def update_details(sender, instance,  **kwargs):
        site = Site.objects.get(id=1)
        site.categories -=1
        site.save()
        # del_inv  = Inventory.objects.get(product=instance)
        # del_inv.delete()



class Brand(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=25)
    description = models.TextField(max_length=500)
    category = models.ManyToManyField(Category, related_name='brands')
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    count = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.slug:
            self.slug = arabic_to_english_slug(self.name)
        super(Brand, self).save(*args, **kwargs)
        self.count.brands += 1
        self.count.save()
        
    
    def delete(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        self.count.brands -= 1
        self.count.save()



class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    count = models.ForeignKey(Site, on_delete=models.SET_DEFAULT, default=1)
    image = ResizedImageField(size=[300, 300], upload_to='images', null= True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.slug:
            self.slug = arabic_to_english_slug(self.name)
        super(Product, self).save(*args, **kwargs)
        
    @property
    def price(self):
        return self.prices.last().value*(100 - self.prices.last().discount)/100
    
    
@receiver(post_save, sender =  Product)
def update_details(sender, instance, created, **kwargs):
    if created:
        site = Site.objects.get(id=1)
        site.products +=1
        site.save()
        Inventory.objects.create(product=instance)
    
@receiver(post_delete, sender =  Product)
def update_details(sender, instance,  **kwargs):
        site = Site.objects.get(id=1)
        site.products -=1
        site.save()
        # del_inv  = Inventory.objects.get(product=instance)
        # del_inv.delete()
    
    
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock = models.PositiveBigIntegerField(default=0)
    purchases = models.PositiveBigIntegerField(default=0)
    sales = models.PositiveBigIntegerField(default=0)



class Price(models.Model):
    value = models.FloatField()
    discount = models.PositiveSmallIntegerField(default=0)
    product = models.ForeignKey(Product, related_name='prices', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)




class Spec(models.Model):
    name = models.CharField(max_length=50)
    type = models.IntegerField(choices=[
        (1, 'Numeric'),
        (2, 'Text'),
        (3, 'Boolean'),
    ])
    unit = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='specs', on_delete=models.CASCADE)


class NumSpecs(models.Model):
    value = models.FloatField()
    product = models.ForeignKey(Product, related_name='num_spec', on_delete=models.CASCADE)
    spec = models.ForeignKey(Spec, related_name='num_spec', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(null=True)

class TxtSpecs(models.Model):
    value = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='txt_spec', on_delete=models.CASCADE)
    spec = models.ForeignKey(Spec, related_name='txt_spec', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(null=True)

class BoolSpecs(models.Model):
    value = models.BooleanField(default=False)
    product = models.ForeignKey(Product,  related_name='bool_spec', on_delete=models.CASCADE)
    spec = models.ForeignKey(Spec, related_name='bool_spec', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(null=True)