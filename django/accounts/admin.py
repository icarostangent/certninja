import uuid
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
from accounts import models
from accounts.signals import password_reset_signal, verify_email_signal_signal_signal


admin.site.unregister(User)

class EmailRequiredMixin(object):
    def __init__(self, *args, **kwargs):
        super(EmailRequiredMixin, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

class MyUserCreationForm(EmailRequiredMixin, UserCreationForm):
    pass

class MyUserChangeForm(EmailRequiredMixin, UserChangeForm):
    pass

@admin.register(User)
class EmailRequiredUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    add_fieldsets = ((None, {
        'fields': ('username', 'email', 'password1', 'password2'), 
        'classes': ('wide',)
    }),) 


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
    readonly_fields = ['user', 'email', 'verify_key', 'verification_sent', 'verified', 'reset_key', 'reset_sent']
    actions = ['make_verified', 'send_verification_email', 'send_password_reset']

    @admin.action(description='Mark selected email addresses as verified')
    def make_verified(self, request, queryset):
        queryset.update(verified=True)

    @admin.action(description='Send verification email')
    def send_verification_email(self, request, queryset):
        for email_address in queryset:
            email_address.verify_key = get_random_string(length=32)
            verify_email_signal.send(sender='admin', email=email_address.email, key=email_address.verify_key)
            email_address.verification_sent = timezone.now()
            email_address.save()

    @admin.action(description='Send password reset email')
    def send_password_reset(self, request, queryset):
        for email_address in queryset:
            email_address.reset_key = get_random_string(length=32)
            print(email_address)
            password_reset_signal.send(sender='admin', email=email_address.email, key=email_address.reset_key)
            email_address.reset_sent = timezone.now()
            email_address.save()