# Generated by Django 4.2.7 on 2023-12-03 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('agent_number', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('agent_first_name', models.CharField(max_length=300)),
                ('agent_last_name', models.CharField(max_length=300)),
                ('agent_phone_number', models.IntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('invoice_number', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('sales_date', models.DateField(auto_now_add=True)),
                ('total_sales', models.IntegerField(default=0)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.agent')),
            ],
        ),
    ]
