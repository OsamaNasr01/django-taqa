from django.db import models

# Create your models here.

class Invoice(models.Model):
    name = models.CharField(max_length=255)
    value = models.PositiveIntegerField()

    def __str__(self):
        return self.name