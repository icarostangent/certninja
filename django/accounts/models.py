import uuid
import os
import stripe
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_prometheus.models import ExportModelOperationsMixin


class Subscription(ExportModelOperationsMixin('subscription'), models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255)
    subscription_type = models.CharField(max_length=255, default='starter', choices=[('starter', 'Starter'), ('basic', 'Basic'), ('growth', 'Growth'), ('ultimate', 'Ultimate')])

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created == True:
        stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'django needs a stripe secret key')
        cust = stripe.Customer.create(description=f"{instance.username}",)
        Subscription.objects.create(user=instance, customer_id=cust.id)


class EmailAddress(ExportModelOperationsMixin('email_address'), models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    key = models.UUIDField(default=uuid.uuid4)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    verification_sent = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        unique_together = [("user", "email")]

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def create_email_address(sender, instance, created, **kwargs):
    if created == True:
        EmailAddress.objects.create(user=instance, email=instance.email)
