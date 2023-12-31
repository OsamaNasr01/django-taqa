# Generated by Django 4.2.4 on 2023-12-16 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_category_image'),
        ('members', '0009_remove_address_user'),
        ('tenders', '0003_rename_question_choice_question_alter_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenderrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='TenderOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0)),
                ('submit', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tender_offers', to='members.company')),
                ('request', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offers', to='tenders.tenderrequest')),
            ],
        ),
        migrations.CreateModel(
            name='OfferItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.FloatField()),
                ('price', models.FloatField(default=0)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='tenders.tenderoffer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tender_offers', to='products.product')),
            ],
        ),
    ]
