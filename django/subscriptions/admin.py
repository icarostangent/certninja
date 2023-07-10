from django.contrib import admin
from subscriptions.models import StripeCustomer


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    readonly_fields = []