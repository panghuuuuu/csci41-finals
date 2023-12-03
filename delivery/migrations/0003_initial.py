# Generated by Django 4.2.7 on 2023-12-03 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
        ('delivery', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivered_orders', to='staff.order'),
        ),
    ]
