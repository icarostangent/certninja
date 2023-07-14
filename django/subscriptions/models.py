from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class StripeCustomer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.pk} - {self.user.username}"


@receiver(post_save, sender=User)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created == True:
        StripeCustomer.objects.create(user=instance)


class StripeProduct(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name