# Generated by Django 4.0.4 on 2022-05-15 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreFunctionality', '0002_item_category_item_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='template'),
        ),
    ]
