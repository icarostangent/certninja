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

obj = r.lpop('domains_register')
if obj:
    json_obj = json.loads(obj)
    print(f'[*] got job from redis {json_obj}')
    ip = json_obj['ip'].split(':')[0]
    try:
        port = json_obj['ip'].split(':')[1]
    except IndexError:
        port = 443

    output = sslcheck.connect(json_obj['domain'], ip=ip, port=port)
    print(f'[*] Completed job {output}')

    db.run({
        'author_id': json_obj['author_id'],
        'domain_id': json_obj['domain_id'],
        'domain': json_obj['domain'],
        'ip': json_obj['ip'],
        'output': output,
    })
    print(f'[*] Resetting scan status on domain id {json_obj["domain_id"]}')
    # db.set_scan_status('complete', json_obj['domain_id'])
