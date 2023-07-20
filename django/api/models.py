import os
import stripe
import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=100, blank=True)

# @receiver(post_save, sender=User )
# def create_account(sender, instance, created, **kwargs):
#     if created:
#         print(instance)
#         # account = Account.create(user=instance.user)


class Domain(models.Model):
    user = models.ForeignKey(User, related_name='domains', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    last_scan = models.TextField(blank=True, null=True)
    scan_status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Scan(models.Model):
    user = models.ForeignKey(User, related_name='scans', on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, related_name='scans', on_delete=models.CASCADE)
    uuid = models.CharField(max_length=255, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    last_scan = models.TextField()
    
    def __str__(self):
        return str(self.uuid)


class StripeCustomer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255)
    subscription_type = models.CharField(max_length=255, default='starter', choices=[('starter', 'Starter'), ('basic', 'Basic'), ('growth', 'Growth'), ('ultimate', 'Ultimate')])

    def __str__(self):
        return f"{self.user.pk}-{self.user.username}"


@receiver(post_save, sender=User)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created == True:
        stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'django needs a stripe secret key')
        cust = stripe.Customer.create(description=f"{instance.pk}-{instance.username}",)
        StripeCustomer.objects.create(user=instance, customer_id=cust.id)


class StripeProduct(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    product_id = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.name