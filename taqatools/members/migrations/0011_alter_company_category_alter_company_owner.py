# Generated by Django 4.2.4 on 2023-12-28 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0010_alter_company_address_alter_company_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='category',
            field=models.ManyToManyField(null=True, related_name='companies', to='members.cocategory'),
        ),
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL),
        ),
    ]
