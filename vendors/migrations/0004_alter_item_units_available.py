# Generated by Django 4.2.1 on 2023-05-27 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_item_quantity_purchased_item_units_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='units_available',
            field=models.IntegerField(default=models.IntegerField()),
        ),
    ]
