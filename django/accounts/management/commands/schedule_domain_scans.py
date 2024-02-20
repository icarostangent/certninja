import json
import redis
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from django.utils import timezone


class Command(BaseCommand):
    help = "Figure out which domains are due and schedule a scan"

    def add_arguments(self, parser):
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
        now = timezone.now()
        for user in User.objects.all():
            if user.subscription.subscription_active == False:
                # self.stdout.write(self.style.WARNING(f'[*] {now} User subscription inactive: {user}'))
                continue
            for domain in list(user.domains.all())[:settings.DOMAIN_LIMITS[user.subscription.subscription_type]]:
                if not domain.scan_status: 
                    print(f'[+] {domain.name} status empty')
                    domain.scan_status = 'pending'
                    domain.save()
                    r.rpush(settings.REDIS_DOMAIN_REGISTER, json.dumps(model_to_dict(domain)))
                    self.stdout.write(self.style.SUCCESS(f'[+] {now} Found new domain for user {user}: {domain.name}'))
                elif domain.modified < now - relativedelta(minutes=5) and domain.scan_status != 'pending':
                    domain.scan_status = 'pending'
                    domain.save()
                    r.rpush(settings.REDIS_DOMAIN_REGISTER, json.dumps(model_to_dict(domain)))
                    self.stdout.write(self.style.SUCCESS(f'[+] {now} Found job for user {user}: {domain.name}'))
                # else:
                #     self.stdout.write(self.style.WARNING(f'[*] {now} No jobs found.'))

