# Generated by Django 3.0.5 on 2020-05-09 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='payments',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
