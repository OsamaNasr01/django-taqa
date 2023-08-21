# Generated by Django 4.2.4 on 2023-08-20 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0013_alter_cartitem_price_alter_credit_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='credit',
            name='value',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='depit',
            name='value',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='offeritem',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='purchaseinvoiceitem',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='saleinvoiceitem',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]