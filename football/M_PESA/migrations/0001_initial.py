# Generated by Django 3.0.5 on 2020-05-14 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mpesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('transaction_code', models.CharField(max_length=150)),
                ('result_code', models.CharField(max_length=10)),
                ('merchant_id', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'tbl_mpesa',
            },
        ),
    ]
