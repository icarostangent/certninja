from django.contrib import admin
from accounts import models


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = []


