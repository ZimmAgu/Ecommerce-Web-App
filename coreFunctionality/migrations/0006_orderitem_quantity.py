# Generated by Django 4.0.4 on 2022-05-16 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreFunctionality', '0005_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]