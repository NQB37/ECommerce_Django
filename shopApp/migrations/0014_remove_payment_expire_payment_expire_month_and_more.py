# Generated by Django 4.2.1 on 2023-05-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0013_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='expire',
        ),
        migrations.AddField(
            model_name='payment',
            name='expire_month',
            field=models.CharField(choices=[('1', '01'), ('2', '02'), ('3', '03'), ('4', '04'), ('5', '05'), ('6', '06'), ('7', '07'), ('8', '08'), ('9', '09'), ('10', '10'), ('11', '11'), ('12', '12')], default='1', max_length=2),
        ),
        migrations.AddField(
            model_name='payment',
            name='expire_year',
            field=models.CharField(choices=[('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')], default='23', max_length=4),
        ),
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Paypal Card', 'Paypal Card')], default='Credit Card', max_length=255),
        ),
    ]
