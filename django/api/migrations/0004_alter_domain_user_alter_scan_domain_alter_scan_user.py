# Generated by Django 4.2.2 on 2023-07-07 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_alter_account_stripe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='scan',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='api.domain'),
        ),
        migrations.AlterField(
            model_name='scan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scans', to=settings.AUTH_USER_MODEL),
        ),
    ]