import json
import redis
from django.conf import settings
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from api.models import Domain


class Command(BaseCommand):
    help = "Figure out which domains are due and perform a scan"

    def add_arguments(self, parser):
        parser.add_argument("id", nargs="+", type=int)

    def handle(self, *args, **options):
        r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
        try:
            domain = Domain.objects.get(id=options['id'][0])
        except:
            self.stdout.write(self.style.ERROR(f'[!] Domain not found'))
        else:
            r.rpush(settings.REDIS_DOMAIN_REGISTER, json.dumps(model_to_dict(domain)))
            self.stdout.write(self.style.SUCCESS(f'[+] Created job for domain: {domain.name}'))
