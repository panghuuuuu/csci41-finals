# Generated by Django 4.2.7 on 2023-12-04 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0001_initial'),
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='delivered_items',
            field=models.ManyToManyField(related_name='delivered_items', to='items.delivereditem'),
        ),
    ]
