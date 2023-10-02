# Generated by Django 4.2.4 on 2023-10-02 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pumpoffers', '0004_alter_pumpofferitem_q'),
    ]

    operations = [
        migrations.CreateModel(
            name='Irrigation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='PowerSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=55)),
            ],
        ),
        migrations.AddField(
            model_name='pumpofferrequest',
            name='irrigation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pumpoffers.irrigation'),
        ),
        migrations.AddField(
            model_name='pumpofferrequest',
            name='power',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pumpoffers.powersource'),
        ),
    ]
