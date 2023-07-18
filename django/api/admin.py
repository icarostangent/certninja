from django.contrib import admin
from api import models


@admin.register(models.Snippet)
class SnippetAdmin(admin.ModelAdmin):
    readonly_fields = [
        'highlighted',
    ]


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = []


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    readonly_fields = []


@admin.register(models.Scan)
class ScanAdmin(admin.ModelAdmin):
    readonly_fields = []


@admin.register(models.StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    readonly_fields = []


@admin.register(models.StripeProduct)
class StripeProductAdmin(admin.ModelAdmin):
    readonly_fields = []