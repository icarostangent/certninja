from django.contrib import admin
from subscriptions.models import StripeCustomer, StripeProduct


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    readonly_fields = []


@admin.register(StripeProduct)
class StripeProductAdmin(admin.ModelAdmin):
    readonly_fields = []