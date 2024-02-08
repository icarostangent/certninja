# Generated by Django 4.2.9 on 2024-02-08 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_domain_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='agent',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='domains', to='api.agent'),
        ),
    ]
