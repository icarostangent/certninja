import json
import redis

from datetime import datetime, timedelta

import db


now = datetime.now()
# for domain in db.get_domains():
#     if domain['post_content_filtered'] != 'pending':
#         if not domain['post_content'] or domain['post_modified'] <= now - timedelta(days=1):
#             print(f'modified: {domain["post_modified"]}')
#             print(f'1 day ago: {now - timedelta(days=1)}')
#             job = {
#                 'domain': domain['post_title'],
#                 'ip': domain['post_excerpt'],
#                 'domain_id': domain['id'],
#                 'author_id': domain['post_author'],
#             }
#             print('found job')
#             print(job)

try:
    r = redis.StrictRedis(host='redis', port=6379,
                        db=0, decode_responses=True)
except Exception as ex:
    print(ex)
    exit(1)

job = r.rpop('deletions_register')
if job:
    job = json.loads(job)
    print('[*] found job')
    print(job)

    # TODO: downgrade

    if 'starter' in job['meta_value']:
        print('[+] Cleaning starter account')
        db.clean(job['user_id'], 'starter')

    if 'basic' in job['meta_value']:
        print('[+] Cleaning basic account')
        db.clean(job['user_id'], 'basic')

    if 'growth' in job['meta_value']:
        print('[+] Cleaning growth account')
        db.clean(job['user_id'], 'growth')

    if 'ultimate' in job['meta_value']:
        print('[+] Cleaning ultimate account')
        db.clean(job['user_id'], 'ultimate')
