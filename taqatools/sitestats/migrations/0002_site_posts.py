# Generated by Django 4.2.4 on 2023-08-28 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitestats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='posts',
            field=models.PositiveIntegerField(default=0),
        ),
    ]