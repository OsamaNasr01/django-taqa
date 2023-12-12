# Generated by Django 4.2.4 on 2023-12-12 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0002_tender_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='Question',
            new_name='question',
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(1, 'رقمي'), (2, 'نصي'), (3, 'نعم او لا')]),
        ),
    ]