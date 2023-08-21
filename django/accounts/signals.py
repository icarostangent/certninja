import os
import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from accounts import models


verify_email_signal = Signal() # args: email, key
password_reset_signal = Signal() # args: email, key


@receiver(post_save, sender=User)
def create_subscription(sender, instance, created, **kwargs):
    if created == True:
        models.Subscription.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_email_address(sender, instance, created, **kwargs):
    if created == True:
        models.EmailAddress.objects.create(user=instance, email=instance.email)


@receiver(verify_email_signal)
def send_verify_email_signal(sender, email, key, **kwargs):
    msg = models.TemplateEmail(
        to=email,
        subject=f'Welcome to {settings.DOMAIN_NAME}',
        template='welcome',
        context={'DOMAIN_NAME': settings.DOMAIN_NAME, 'KEY': key},
        from_email=f'admin@{settings.DOMAIN_NAME}',
    )
    msg.send()


@receiver(password_reset_signal)
def send_password_reset_email(sender, email, key, **kwargs):
    msg = models.TemplateEmail(
        to=email,
        subject=f'Welcome to {settings.DOMAIN_NAME}',
        template='reset',
        context={'DOMAIN_NAME': settings.DOMAIN_NAME, 'KEY': key},
        from_email=f'admin@{settings.DOMAIN_NAME}',
    )
    msg.send()