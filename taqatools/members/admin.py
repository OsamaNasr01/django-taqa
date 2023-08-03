from django.contrib import admin
from .models import Company, CoCategory

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Company, CompanyAdmin)
admin.site.register(CoCategory)