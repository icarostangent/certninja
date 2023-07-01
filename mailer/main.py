import json
import os
import redis
import smtplib
import ssl
import time

from email.message import EmailMessage
from email.parser import Parser
from email.policy import default


SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
TARGET_URL = os.environ.get('TARGET_URL')


try:
    r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
    # print('[*] connect to redis')
except Exception as ex:
    print(ex)
    exit(1)

obj = r.lpop('new_user_register')
if obj:
    json_obj = json.loads(obj)
    print(f'[*] got job from redis {json_obj}')

    msg = EmailMessage()
    msg.set_content(f"""
    Activate your account with SSL Checker
    {TARGET_URL}/activate?id={json_obj['id']}&key={json_obj['user_activation_key']}

    {json_obj['registered']}

    """)
    msg['Subject'] = f'Hello {json_obj["username"]}!'
    msg['From'] = SMTP_USER
    msg['To'] = json_obj['email']

    try:
        print('[*] establishing smtp connection')
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ssl.create_default_context()) as server:
            print(f'[+] sending message to {json_obj["email"]}')
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except Exception as ex:
        print('[!] failed to establish smtp connection')
        print(ex)
        exit(1)

obj = r.lpop('password_reset_register')
if obj:
    json_obj = json.loads(obj)
    print(f'[*] got job from redis {json_obj}')

    msg = EmailMessage()
    msg.set_content(f"""
    Click here to reset your password.
    {TARGET_URL}/reset?id={json_obj['id']}&key={json_obj['reset_key']}


    """)
    msg['Subject'] = f'Hello {json_obj["username"]}!'
    msg['From'] = SMTP_USER
    msg['To'] = json_obj['email']

    try:
        print('[*] establishing smtp connection')
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ssl.create_default_context()) as server:
            print(f'[+] sending message to {json_obj["email"]}')
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except Exception as ex:
        print('[!] failed to establish smtp connection')
        print(ex)
        exit(1)

