# Generated by Django 4.2.7 on 2023-12-03 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_name', models.CharField(max_length=300, primary_key=True, serialize=False)),
                ('client_office_address', models.CharField(max_length=300)),
                ('client_email_address', models.EmailField(max_length=254)),
            ],
        ),
    ]
