import uuid
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import TemplateDoesNotExist, render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django_prometheus.models import ExportModelOperationsMixin
from api.signals import verify_email_signal


class Agent(ExportModelOperationsMixin('agent'), models.Model):
    user = models.ForeignKey(User, related_name='agents', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, default=None, null=True, blank=True)
    last_seen = models.DateTimeField(default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.api_key = get_random_string(length=32)
        super(Agent, self).save(*args, **kwargs)


class Domain(ExportModelOperationsMixin('domain'), models.Model):
    user = models.ForeignKey(User, related_name='domains', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    port = models.IntegerField(default=443, blank=True, null=True)
    last_scan = models.TextField(blank=True, null=True)
    last_scan_error = models.TextField(blank=True, null=True)
    scan_status = models.CharField(max_length=100, blank=True, null=True)
    agent = models.OneToOneField(Agent, related_name='domains', blank=True, null=True, on_delete=models.PROTECT)
    scan_now_last_accessed = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Scan(ExportModelOperationsMixin('scan'), models.Model):
    user = models.ForeignKey(User, related_name='scans', on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, related_name='scans', on_delete=models.CASCADE)
    uuid = models.CharField(max_length=255, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    activity = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    output = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    common_name = models.CharField(max_length=255, blank=True, null=True)
    issuer = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    not_after = models.DateTimeField(blank=True, null=True)
    not_before = models.DateTimeField(blank=True, null=True)
    alt_names = models.TextField(blank=True, null=True)
    signature_algorithm = models.CharField(max_length=255, blank=True, null=True)
    raw = models.TextField(blank=True, null=True)
    error = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.domain)

    
class EmailAddress(ExportModelOperationsMixin('email_address'), models.Model):
    user = models.ForeignKey(User, related_name='emails', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    domain = models.ForeignKey(Domain, related_name='emails', on_delete=models.CASCADE)

    class Meta:
        unique_together = [("user", "email")]
        ordering = ['-created']

    def __str__(self):
        return self.email


class Subscription(ExportModelOperationsMixin('subscription'), models.Model):
    user = models.OneToOneField(User, related_name='subscription', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=255, default='')
    client_reference_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255, default='')
    subscription_type = models.CharField(
        max_length=255, 
        default=settings.STRIPE_PRODUCT_CHOICES[0][0], 
        choices=settings.STRIPE_PRODUCT_CHOICES
    )
    subscription_active = models.BooleanField(default=True)
    period_start = models.DateTimeField(default=None, blank=True, null=True)
    period_end = models.DateTimeField(default=None, blank=True, null=True)
    previous_subscription_type = models.CharField(
        max_length=255, 
        default=settings.STRIPE_PRODUCT_CHOICES[0][0], 
        choices=settings.STRIPE_PRODUCT_CHOICES
    )
    cancel_at = models.DateTimeField(default=None, blank=True, null=True)
    cancel_at_period_end = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        self.client_reference_id = get_random_string(length=32)
        super(Subscription, self).save(*args, **kwargs)


class TemplateEmail:
    def __init__(
        self,
        to,
        subject,
        template,
        context={},
        from_email=None,
        reply_to=None,
        **email_kwargs,
    ):
        self.to = to
        self.subject = subject
        self.template = template
        self.context = context
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        self.reply_to = reply_to
        self.context["template"] = template
        self.html_content, self.plain_content = self.render_content()
        self.to = self.to if not isinstance(self.to, str) else [self.to]

        if self.reply_to:
            self.reply_to = (
                self.reply_to if not isinstance(self.reply_to, str) else [self.reply_to]
            )

        self.django_email = EmailMultiAlternatives(
            subject=self.subject,
            body=self.plain_content,
            from_email=self.from_email,
            to=self.to,
            reply_to=self.reply_to,
            **email_kwargs,
        )
        self.django_email.attach_alternative(self.html_content, "text/html")

    def render_content(self):
        html_content = self.render_html()
        try:
            plain_content = self.render_plain()
        except TemplateDoesNotExist:
            plain_content = strip_tags(html_content)

        return html_content, plain_content

    def render_plain(self):
        return render_to_string(self.get_plain_template_name(), self.context)

    def render_html(self):
        return render_to_string(self.get_html_template_name(), self.context)

    def get_plain_template_name(self):
        return f"email/{self.template}.txt"

    def get_html_template_name(self):
        return f"email/{self.template}.html"

    def send(self, **send_kwargs):
        return self.django_email.send(**send_kwargs)