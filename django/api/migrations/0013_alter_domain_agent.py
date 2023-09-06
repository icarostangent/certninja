# Generated by Django 3.2.20 on 2023-08-24 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_domain_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='domains', to='api.agent'),
        ),
    ]