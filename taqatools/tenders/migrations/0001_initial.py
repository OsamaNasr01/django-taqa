# Generated by Django 4.2.4 on 2023-12-09 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0009_remove_address_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0012_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TenderRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenders', to='members.address')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='tenders.tender')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tender_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TenderCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenders', to='products.category')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='tenders.tender')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=155)),
                ('type', models.IntegerField(choices=[(1, 'Numeric'), (2, 'Text'), (3, 'Boolean')])),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='tenders.tender')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=55)),
                ('Question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='tenders.question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='tenders.question')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='tenders.tenderrequest')),
            ],
        ),
    ]
