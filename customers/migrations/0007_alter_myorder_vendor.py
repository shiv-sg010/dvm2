# Generated by Django 4.2.1 on 2023-05-27 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_myorder_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myorder',
            name='vendor',
            field=models.TextField(),
        ),
    ]
