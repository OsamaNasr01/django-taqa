# Generated by Django 5.0 on 2024-01-01 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_spec_name_alter_spec_type_choice_specvalue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='question',
            new_name='spec',
        ),
    ]
