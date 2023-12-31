# Generated by Django 4.2.7 on 2023-12-04 15:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issueditem',
            name='item_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='items.itemtype'),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='item_discount',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
    ]
