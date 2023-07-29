from django.contrib import admin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from accounts import models


admin.site.unregister(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser')


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = [
        'user',
        'customer_id', 
        'subscription_id',
        'created',
    ]


@admin.register(models.EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ['email', 'user', 'verified']
    list_filter = ['verified',]
    search_fields = ['email', 'user__username']
    raw_id_fields = ['user',]
    readonly_fields = ['verification_sent',]
    actions = ['make_verified', 'send_verification_email']

    @admin.action(description='Mark selected email addresses as verified')
    def make_verified(self, request, queryset):
        queryset.update(verified=True)

    @admin.action(description='Send verification email')
    def send_verification_email(self, request, queryset):
        for email_address in queryset:
            send_mail('Subject here', 'Here is the message.', 'from@example.com', [email_address.email], fail_silently=False)
            email_address.verification_sent = timezone.now()
            email_address.save()
