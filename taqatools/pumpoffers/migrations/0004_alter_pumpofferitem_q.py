# Generated by Django 4.2.4 on 2023-09-26 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pumpoffers', '0003_alter_pumpoffer_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pumpofferitem',
            name='q',
            field=models.FloatField(),
        ),
    ]
