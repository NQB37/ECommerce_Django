# Generated by Django 4.2.1 on 2023-05-23 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0015_order_address_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
