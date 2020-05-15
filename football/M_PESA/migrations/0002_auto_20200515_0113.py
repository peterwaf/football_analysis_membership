# Generated by Django 3.0.5 on 2020-05-14 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('M_PESA', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mpesa',
            options={'verbose_name_plural': 'MPesa'},
        ),
        migrations.AddField(
            model_name='mpesa',
            name='amount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
