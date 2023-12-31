# Generated by Django 4.2.7 on 2023-12-04 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('supplier', '0001_initial'),
        ('client', '0001_initial'),
        ('agent', '0001_initial'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier'),
        ),
        migrations.AddField(
            model_name='issuer',
            name='staff',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='issuance',
            name='agent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.agent'),
        ),
        migrations.AddField(
            model_name='issuance',
            name='batch_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.batchinventory'),
        ),
        migrations.AddField(
            model_name='issuance',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client'),
        ),
        migrations.AddField(
            model_name='issuance',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.issuer'),
        ),
    ]
