# Generated by Django 4.2.9 on 2024-02-17 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_scan_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='signature_algorithm',
            field=models.CharField(max_length=255, null=True),
        ),
    ]