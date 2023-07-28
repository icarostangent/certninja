from allauth.account.adapter import DefaultAccountAdapter
from api.tasks import send_activation_email

class AccountAdapter(DefaultAccountAdapter):
    pass
    # def send_mail(self, template_prefix, email, context):
    #     print('lol got here')
    #     send_activation_email.delay(self.render_mail(template_prefix, email, context))