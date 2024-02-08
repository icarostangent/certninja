import json
import redis
from datetime import datetime

import db
import sslcheck

try:
    print(f'[*] scanner connect to redis {datetime.now()}')
    r = redis.StrictRedis(host='redis', port=6379,
                            db=0, decode_responses=True)
except Exception as ex:
    print(ex)
    exit(1)

job = r.lpop('domains_register')
if job:
    domain = json.loads(job)
    print(f'[*] got job from redis {domain}')

    if domain['ip_address']:
        ip = domain['ip_address']
    else:
        ip = ''
    
    if domain['port']:
        port = domain['port']
    else:
        port = 443

    output = sslcheck.connect(domain['name'], ip=ip, port=port)
    print(f'[*] Completed job {output}')

    db.insert({
        'user_id': domain['user'],
        'domain_id': domain['id'],
        'domain': domain['name'],
        'ip': domain['ip_address'],
        'port': domain['port'],
        'output': output,
    })
    # print(f'[*] Resetting scan status on domain id {domain["domain_id"]}')
    # db.set_scan_status('complete', domain['domain_id'])
