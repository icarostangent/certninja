import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string
from django_prometheus.models import ExportModelOperationsMixin


class Agent(ExportModelOperationsMixin('agent'), models.Model):
    user = models.ForeignKey(User, related_name='agents', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, default=None, null=True, blank=True)
    last_seen = models.DateTimeField(default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.api_key = get_random_string(length=32)
        super(Agent, self).save(*args, **kwargs)


class Domain(ExportModelOperationsMixin('domain'), models.Model):
    user = models.ForeignKey(User, related_name='domains', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    last_scan = models.TextField(blank=True, null=True)
    scan_status = models.CharField(max_length=100, blank=True, null=True)
    agent = models.ForeignKey(Agent, related_name='domains', blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Scan(ExportModelOperationsMixin('scan'), models.Model):
    user = models.ForeignKey(User, related_name='scans', on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, related_name='scans', on_delete=models.CASCADE)
    uuid = models.CharField(max_length=255, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    output = models.TextField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.uuid)
