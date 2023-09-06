from django.db import models
from django.contrib.auth.models import User
from products.models import Category
from django.utils.text import slugify
from sitestats.models import Site
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ckeditor.fields import RichTextField
import readtime 

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
        '/':'-',
        # Add more mappings here
    }
    # Create a new string that replaces the Arabic characters with their corresponding English characters
    english_text = ''.join([arabic_to_english_map.get(char, char) for char in text])
    # Use the Django slugify function to generate the slug from the English text
    slug = slugify(english_text)
    return slug

class Tag(models.Model):
    name = models.CharField(max_length=150)
    



class Post(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    auther = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    slug = models.SlugField(unique=True, max_length=255, null=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.slug:
            self.slug = arabic_to_english_slug(self.title)
        super(Post, self).save(*args, **kwargs)
    
    @property
    def timeToRead(self):
        return readtime.of_html(self.content, wpm=150)
        
        

@receiver(post_save, sender =  Post)
def update_details(sender, instance, created, **kwargs):
    if created:
        site = Site.objects.get(id=1)
        site.posts +=1
        site.save()
    
@receiver(post_delete, sender =  Post)
def update_details(sender, instance,  **kwargs):
        site = Site.objects.get(id=1)
        site.posts -=1
        site.save()
        # del_inv  = Inventory.objects.get(product=instance)
        # del_inv.delete()