# Generated by Django 4.2.9 on 2024-02-25 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_domain_scan_now_last_accessed_delete_scannow'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailaddress',
            name='domain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='api.domain'),
            preserve_default=False,
        ),
    ]
