from django.contrib import admin
from api.models import Account, Domain, Scan, Snippet, StripeCustomer, StripeProduct


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    readonly_fields = [
        'highlighted',
    ]

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = []

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    readonly_fields = []

@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    readonly_fields = []

@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    readonly_fields = []


@admin.register(StripeProduct)
class StripeProductAdmin(admin.ModelAdmin):
    readonly_fields = []