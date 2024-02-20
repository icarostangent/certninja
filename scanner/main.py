import json
import os
import pytz
import redis
import requests
from datetime import datetime

import db
import sslcheck

ENDPOINT = f"{os.environ.get('TARGET_URL')}/api/service/scans/"
TOKEN = os.environ.get('SCANNER_TOKEN')

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
    print(f"[*] got job from redis {domain['name']}")

    if domain['ip_address']:
        ip = domain['ip_address']
    else:
        ip = ''
    
    if domain['port']:
        port = domain['port']
    else:
        port = 443

    output = sslcheck.connect(domain['name'], ip=ip, port=port)

    json_output = json.loads(output)
    headers = {
        'Authorization': f'Token {TOKEN}',
        'Content-Type': 'application/json',
    }
    print('json', json_output)

    if 'error' in json_output:
        print(f"error: {json_output['error']}")
        resp = requests.post(ENDPOINT, headers=headers, json={
            'user': domain['user'],
            'domain': domain['id'],
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
        print(f"no errror")
        not_after = datetime.strptime(json_output['certificate']['notAfter'], "%b %d %H:%M:%S %Y %Z")
        not_after.replace(tzinfo=pytz.UTC)
        not_before = datetime.strptime(json_output['certificate']['notBefore'], "%b %d %H:%M:%S %Y %Z")
        not_before.replace(tzinfo=pytz.UTC)

        resp = requests.post(ENDPOINT, headers=headers, json={
            'user': domain['user'],
            'domain': domain['id'],
            # 'domain': domain['name'],
            'ip': domain['ip_address'],
            'port': domain['port'],
            'output': output,
            'alt_names': ', '.join([name[1] for name in json_output['certificate']['subjectAltName']]),
            'common_name': json_output['certificate']['subject'][0][0][1],
            'issuer': json_output['certificate']['issuer'][1][0][1],
            'not_after': str(not_after),
            'not_before': str(not_before),
            'serial_number': json_output['certificate']['serialNumber'],
            'signature_algorithm': json_output['cipher'][0],
            'error': '',
        })

    print(resp.status_code, resp.text)