# Generated by Django 4.2.9 on 2024-02-25 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailaddress',
            name='reset_key',
        ),
        migrations.RemoveField(
            model_name='emailaddress',
            name='reset_sent',
        ),
        migrations.RemoveField(
            model_name='emailaddress',
            name='verification_sent',
        ),
        migrations.RemoveField(
            model_name='emailaddress',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='emailaddress',
            name='verify_key',
        ),
    ]
