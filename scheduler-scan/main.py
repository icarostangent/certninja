import json
import redis

from datetime import datetime
from dateutil.relativedelta import relativedelta

import db


now = datetime.now()
print(f'[*] scheduler executing {now}')
for domain in db.get_domains():
    if domain['scan_status'] == 'pending':
        print(f'[*] pending job... {domain["id"]}')
    else:
        subscription = db.get_user_subscription(domain['user_id'])
        job = {
            'domain': domain['name'],
            'ip': domain['ip_address'],
            'port': domain['port'],
            'domain_id': domain['id'],
            'author_id': domain['user_id'],
        }
        if 'starter' in subscription:
            if not domain['last_scan'] or domain['modified'] <= now - relativedelta(months=1):
                print('[+] found starter job')
                print(job)

                try:
                    r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
                except Exception as ex:
                    print(ex)
                    exit(1)

                r.rpush('domains_register', json.dumps(job))
                db.set_scan_status('pending', domain['id'])

        elif 'basic' in subscription:
            if not domain['last_scan'] or domain['modified'] <= now - relativedelta(weeks=1):
                print('[+] found basic job')
                print(job)

                try:
                    r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
                except Exception as ex:
                    print(ex)
                    exit(1)

                r.rpush('domains_register', json.dumps(job))
                db.set_scan_status('pending', domain['pk'])

        elif 'growth' in subscription:
            if not domain['last_scan'] or domain['modified'] <= now - relativedelta(days=1):
                print('[+] found growth job')
                print(job)

                try:
                    r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
                except Exception as ex:
                    print(ex)
                    exit(1)

                r.rpush('domains_register', json.dumps(job))
                db.set_scan_status('pending', domain['id'])

        elif 'ultimate' in subscription:
            if not domain['last_scan'] or domain['modified'] <= now - relativedelta(hours=1):
                print('[+] found ultimate job')
                print(job)

                try:
                    r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
                except Exception as ex:
                    print(ex)
                    exit(1)

                r.rpush('domains_register', json.dumps(job))
                db.set_scan_status('pending', domain['id'])

        else:
            print('[!] No valid user subscription detected')