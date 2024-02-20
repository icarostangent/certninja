# Generated by Django 4.2.9 on 2024-02-18 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_scan_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='activity',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='serial_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
