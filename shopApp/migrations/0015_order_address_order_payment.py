# Generated by Django 4.2.1 on 2023-05-23 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0014_remove_payment_expire_payment_expire_month_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shopApp.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shopApp.payment'),
        ),
    ]