import json
import redis

from datetime import datetime, timedelta

import db


roles = ['starter', 'basic', 'growth', 'ultimate']
accounts = db.get_accounts()
for role in roles:
    account_types = db.get_account_types(role)
    print('[*] account types')
    print(account_types)
    for account_type in account_types:
        account = [account for account in accounts if account['post_author'] == account_type['user_id']][0]
        downgrade = account['post_password'] == 'true'
        if downgrade:
            print('[+] Downgrade account')
            print(account)
        if not downgrade:
            job = account_type
            try:
                print('[+] Creating job')
                print(job)
                r = redis.StrictRedis(host='redis', port=6379,
                                    db=0, decode_responses=True)
            except Exception as ex:
                print(ex)
                exit(1)

            r.rpush('deletions_register', json.dumps(job))
        