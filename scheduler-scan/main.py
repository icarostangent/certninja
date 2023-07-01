import json
import redis

from datetime import datetime
from dateutil.relativedelta import relativedelta

import db


now = datetime.now()
print(f'[*] scheduler executing {now}')
for domain in db.get_domains():
    if domain['post_content_filtered'] == 'pending':
        print(f'[*] pending job... {domain["id"]}')
    else:
        role = db.get_user_role(domain['post_author'])
        if 'starter' in role:
            if not domain['post_content'] or domain['post_modified'] <= now - relativedelta(months=1):
                # print(f'modified: {domain["post_modified"]}')
                job = {
                    'domain': domain['post_title'],
                    'ip': domain['post_excerpt'],
                    'domain_id': domain['id'],
                    'author_id': domain['post_author'],
                }
                print('[+] found starter job')
                print(job)

                try:
                    r = redis.StrictRedis(host='redis', port=6379,
                                        db=0, decode_responses=True)
                except Exception as ex:
                    print(ex)
                    exit(1)

                ret = r.rpush('domains_register', json.dumps(job))
                db.set_scan_status('pending', domain['id'])

        elif 'basic' in role:
            if not domain['post_content'] or domain['post_modified'] <= now - relativedelta(weeks=1):
                # print(f'modified: {domain["post_modified"]}')
                job = {
                    'domain': domain['post_title'],
                    'ip': domain['post_excerpt'],
                    'domain_id': domain['id'],
                    'author_id': domain['post_author'],
                }
                print('[+] found basic job')
                print(job)

                try:
                    r = redis.StrictRedis(host='redis', port=6379,
                                        db=0, decode_responses=True)
                except Exception as ex:
                    print(ex)
                    exit(1)

                r.rpush('domains_register', json.dumps(job))
                db.set_scan_status('pending', domain['id'])

        elif 'growth' in role:
            if not domain['post_content'] or domain['post_modified'] <= now - relativedelta(days=1):
                # print(f'modified: {domain["post_modified"]}')
                job = {
                    'domain': domain['post_title'],
                    'ip': domain['post_excerpt'],
                    'domain_id': domain['id'],
                    'author_id': domain['post_author'],
                }
                print('[+] found growth job')
                print(job)

                try:
                    r = redis.StrictRedis(host='redis', port=6379,
                                        db=0, decode_responses=True)
                except Exception as ex:
                    print(ex)
                    exit(1)

                r.rpush('domains_register', json.dumps(job))
                db.set_scan_status('pending', domain['id'])

        elif 'ultimate' in role:
            if not domain['post_content'] or domain['post_modified'] <= now - relativedelta(hours=1):
                # print(f'modified: {domain["post_modified"]}')
                job = {
                    'domain': domain['post_title'],
                    'ip': domain['post_excerpt'],
                    'domain_id': domain['id'],
                    'author_id': domain['post_author'],
                }
                print('[+] found ultimate job')
                print(job)

                try:
                    r = redis.StrictRedis(host='redis', port=6379,
                                        db=0, decode_responses=True)
                except Exception as ex:
                    print(ex)
                    exit(1)

                r.rpush('domains_register', json.dumps(job))
                db.set_scan_status('pending', domain['id'])

                print(job)

               

        else:
            print('[!] No valid user role detected')