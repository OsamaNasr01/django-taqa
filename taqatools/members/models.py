from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.text import slugify


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
    website = models.URLField(max_length=200)
    address = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    category = models.ManyToManyField(CoCategory, related_name='companies')
    slug = models.SlugField(max_length=150, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.slug:
            self.slug = arabic_to_english_slug(self.name)
        super(Company, self).save(*args, **kwargs)
