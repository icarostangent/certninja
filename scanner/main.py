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
    json_obj = json.loads(job)
    print(f'[*] got job from redis {json_obj}')

    if json_obj['ip']:
        ip = json_obj['ip']
    else:
        ip = ''
    
    if json_obj['port']:
        port = json_obj['port']
    else:
        port = 443

    output = sslcheck.connect(json_obj['domain'], ip=ip, port=port)
    print(f'[*] Completed job {output}')

    db.insert({
        'author_id': json_obj['author_id'],
        'domain_id': json_obj['domain_id'],
        'domain': json_obj['domain'],
        'ip': json_obj['ip'],
        'output': output,
    })
    # print(f'[*] Resetting scan status on domain id {json_obj["domain_id"]}')
    # db.set_scan_status('complete', json_obj['domain_id'])
