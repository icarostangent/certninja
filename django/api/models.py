import uuid
from django.contrib.auth.models import User
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class Domain(ExportModelOperationsMixin('domain'), models.Model):
    user = models.ForeignKey(User, related_name='domains', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    last_scan = models.TextField(blank=True, null=True)
    scan_status = models.CharField(max_length=100, blank=True, null=True)

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
