# Generated by Django 3.0.5 on 2020-05-29 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_payments_phone_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payments',
            options={'verbose_name_plural': 'Payments'},
        ),
    ]