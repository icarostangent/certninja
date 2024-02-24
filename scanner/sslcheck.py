#!/usr/bin/python3

import json
import sys
from urllib.request import ssl, socket


def connect(domain, port=443, ip=''):
    """
    Connects to server to identify TLS certificate meta.

    Accepts domain and optional port number and returns json.
    """
    print(f'[+] Initiating scan {domain} {ip}:{port}')

    if not ip:
        try:
            ip = socket.gethostbyname(domain)
        except socket.gaierror as ex:
            # print({ 'error': 'dns lookup failed', 'ex': ex  })
            return json.dumps({ 'error': 'DNS lookup failed', 'ex': str(ex)  })

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((ip, port)) as sock:
            sock.settimeout(5)
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                return json.dumps({
                    'certificate': ssock.getpeercert(),
                    'cipher': ssock.cipher(),
                })

    except ssl.SSLEOFError as ex:
        # print({ 'error': 'SSL EOF error', 'ex': ex })
        return json.dumps({ 'error': 'SSL EOF error', 'ex': str(ex)  })

    except ssl.SSLCertVerificationError as ex:
        # print({ 'error': ex })
        return json.dumps({ 'error': 'Certificate verify failed', 'ex': str(ex)  })

    except Exception as ex:
        print(ex)
        return json.dumps({ 'error': str(ex) })

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(connect(sys.argv[1]))
    elif len(sys.argv) == 3:
        ip = sys.argv[2].split(':')[0]
        try:
            port = sys.argv[2].split(':')[1]
        except IndexError:
            port = 443
        print(connect(sys.argv[1], ip=ip, port=port))
    else:
        print("usage: python sslcheck.py hostname ip (optional)")
        sys.exit(1)
