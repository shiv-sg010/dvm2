# Generated by Django 4.2.1 on 2023-05-26 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_cart_date_purchased'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='date_purchased',
        ),
    ]
