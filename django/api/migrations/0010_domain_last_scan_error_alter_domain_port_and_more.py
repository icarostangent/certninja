# Generated by Django 4.2.9 on 2024-02-22 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_scan_activity_alter_scan_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='last_scan_error',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='domain',
            name='port',
            field=models.IntegerField(blank=True, default=443, null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='alt_names',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='common_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='error',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='issuer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='not_after',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='not_before',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='raw',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='signature_algorithm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
