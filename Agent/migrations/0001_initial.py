# Generated by Django 4.2.7 on 2023-11-26 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('agent_number', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('agent_first_name', models.CharField(max_length=300)),
                ('agent_last_name', models.CharField(max_length=300)),
                ('agent_phone_number', models.IntegerField()),
            ],
        ),
    ]
