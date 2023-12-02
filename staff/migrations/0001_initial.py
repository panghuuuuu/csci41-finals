# Generated by Django 4.2.7 on 2023-12-02 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BatchInventory',
            fields=[
                ('batch_number', models.AutoField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issuance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(auto_now_add=True)),
                ('issue_time', models.TimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issuer',
            fields=[
                ('issuer_number', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_number', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('staff_first_name', models.CharField(max_length=300)),
                ('staff_last_name', models.CharField(max_length=300)),
                ('staff_phone_number', models.IntegerField()),
                ('staff_type', models.CharField(choices=[('Regular', 'Regular'), ('Issuer', 'Issuer'), ('Receiver', 'Receiver')], max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('receiver_number', models.AutoField(primary_key=True, serialize=False)),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='staff.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_number', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('order_time', models.TimeField(auto_now_add=True)),
                ('isDelivered', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.receiver')),
            ],
        ),
    ]
