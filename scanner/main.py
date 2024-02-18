import json
import pytz
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
    # print(f'[*] Completed job {output}')

    json_output = json.loads(output)

    if 'error' in json_output:
        print('found error')
        db.insert({
            'user_id': domain['user'],
            'domain_id': domain['id'],
            'domain': domain['name'],
            'ip': domain['ip_address'],
            'port': domain['port'],
            'output': output,
            'alt_names': None,
            'common_name': None,
            'issuer': None,
            'not_after': None,
            'not_before': None,
            'serial_number': None,
            'signature_algorithm': None,
            'error': json_output['error'],
        })
    else:
        print('no error')
        print(json_output['cipher'])

        not_after = datetime.strptime(json_output['certificate']['notAfter'], "%b %d %H:%M:%S %Y %Z")
        not_after.replace(tzinfo=pytz.UTC)
        not_before = datetime.strptime(json_output['certificate']['notBefore'], "%b %d %H:%M:%S %Y %Z")
        not_before.replace(tzinfo=pytz.UTC)

        db.insert({
            'user_id': domain['user'],
            'domain_id': domain['id'],
            'domain': domain['name'],
            'ip': domain['ip_address'],
            'port': domain['port'],
            'output': output,
            'alt_names': ', '.join([name[1] for name in json_output['certificate']['subjectAltName']]),
            'common_name': json_output['certificate']['subject'][0][0][1],
            'issuer': json_output['certificate']['issuer'][1][0][1],
            'not_after': not_after,
            'not_before': not_before,
            'serial_number': json_output['certificate']['serialNumber'],
            'signature_algorithm': json_output['cipher'][0],
            'error': '',
        })

    # print(f'[*] Resetting scan status on domain id {domain["domain_id"]}')
    # db.set_scan_status('complete', domain['domain_id'])
