# Generated by Django 4.2.1 on 2023-05-26 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_remove_item_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity_purchased',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='units_available',
            field=models.IntegerField(default=0),
        ),
    ]
