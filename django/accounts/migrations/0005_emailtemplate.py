# Generated by Django 3.2.20 on 2023-07-28 23:58

from django.db import migrations, models
import django_prometheus.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_emailaddress_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('text', models.TextField(blank=True)),
                ('html', models.TextField(blank=True)),
            ],
            bases=(django_prometheus.models.ExportModelOperationsMixin('email_template'), models.Model),
        ),
    ]
