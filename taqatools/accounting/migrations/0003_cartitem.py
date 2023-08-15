# Generated by Django 4.2.4 on 2023-08-12 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_boolspecs_order_numspecs_order_txtspecs_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0002_offer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q', models.PositiveSmallIntegerField()),
                ('price', models.FloatField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart', to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]