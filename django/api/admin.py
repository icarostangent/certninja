from django.contrib import admin
from api.models import Account, Domain, Scan


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = []

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    readonly_fields = []

@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    readonly_fields = []
