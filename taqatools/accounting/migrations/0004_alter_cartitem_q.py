# Generated by Django 4.2.4 on 2023-08-14 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='q',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
