from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy
from api import models


admin.site.unregister(TokenProxy)

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