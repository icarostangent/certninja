from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy
from api import models


@admin.register(models.Agent)
class AgentAdmin(admin.ModelAdmin):
    readonly_fields = []

@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip_address', 'port', 'user']
    readonly_fields = []


@admin.register(models.Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ['domain', 'ip_address', 'port', 'user']
    readonly_fields = ['activity']
