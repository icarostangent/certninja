from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()
    last_scan = models.TextField()

    def __str__(self):
        return self.user.name


class Scan(models.Model):
    user = models.ForeignKey(User, related_name='scans', on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, related_name='domains', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_scan = models.TextField()
    
    def __str__(self):
        return self.user.name
