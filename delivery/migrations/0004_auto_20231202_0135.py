# Generated by Django 3.2 on 2023-12-01 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_initial'),
        ('staff', '0002_initial'),
        ('delivery', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='date',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='delivered_quantity',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='item',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='time',
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivered_items',
            field=models.ManyToManyField(related_name='delivered_items', to='items.DeliveredItem'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivery_date',
            field=models.DateField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivery_time',
            field=models.TimeField(auto_now_add=True, default=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivered_orders', to='staff.order'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='delivery_number',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
