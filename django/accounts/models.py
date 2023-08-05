from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import TemplateDoesNotExist, render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django_prometheus.models import ExportModelOperationsMixin
from accounts.signals import verify_email_signal


class Subscription(ExportModelOperationsMixin('subscription'), models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255)
    subscription_type = models.CharField(max_length=255, default='starter', choices=[('starter', 'Starter'), ('basic', 'Basic'), ('growth', 'Growth'), ('ultimate', 'Ultimate')])

    def __str__(self):
        return f"{self.user.username}"


class EmailAddress(ExportModelOperationsMixin('email_address'), models.Model):
    user = models.OneToOneField(to=User, related_name='email_address', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    verify_key = models.CharField(default=get_random_string(length=32), max_length=255, null=True)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    verification_sent = models.DateTimeField(null=True)
    reset_key = models.CharField(default=None, null=True, max_length=255)
    reset_sent = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        unique_together = [("user", "email")]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.id:
            verify_email_signal.send(sender=self.__class__, email=self.email, key=self.verify_key)
            self.verification_sent = timezone.now()
        super(EmailAddress, self).save(*args, **kwargs)


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