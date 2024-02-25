from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Subscription


class Command(BaseCommand):
    help = "Expire accounts whose subscription is past due by setting subscription.active to False"

    def add_arguments(self, parser):
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        now = timezone.now()
        for sub in Subscription.objects.all():
            if sub.period_end == None:
                continue
            if now >= sub.period_end and sub.subscription_active == True:
                sub.subscription_active = False
                sub.save()
                self.stdout.write(self.style.SUCCESS(f'[+] {now} Expired subscription for account {sub.user}'))