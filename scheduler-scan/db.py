import mysql.connector
import os
import uuid
from datetime import datetime, timedelta

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
database = os.environ.get('DB_DATABASE')

def get_domains():
    try:
        # print('[*] connecting to db')
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    except Exception as ex:
        print(ex)
        exit(1)

    cursor = cnx.cursor()
    stmt = "SELECT * FROM api_domain"
    cursor.execute(stmt)
    domains = [parse_domain(domain) for domain in cursor.fetchall()]
    # print(domains)
    cursor.close()
    cnx.close()

    return domains

def get_user_subscription(id):
    try:
        # print('[*] connecting to db')
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    except Exception as ex:
        print(ex)
        exit(1)

    cursor = cnx.cursor()
    stmt = f"select * from accounts_subscription where user_id = {id}"
    cursor.execute(stmt)
    subscription = [parse_account(user) for user in cursor.fetchall()].pop()['subscription_type']
    cursor.close()
    cnx.close()

    return subscription

def set_scan_status(status, domain_id):
    try:
        # print('[*] connecting to db')
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    except Exception as ex:
        print(ex)
        exit(1)

    cursor = cnx.cursor()
    stmt = f"UPDATE api_domain SET scan_status = '{status}' WHERE id = '{domain_id}'"
    cursor.execute(stmt)
    cnx.commit()
    cursor.close()
    cnx.close()


def parse_domain(domain_raw):
    return {
        'id': domain_raw[0],
        'name': domain_raw[1],
        'created': domain_raw[2],
        'modified': domain_raw[3],
        'ip_address': domain_raw[4],
        'port': domain_raw[5],
        'last_scan': domain_raw[6],
        'scan_status': domain_raw[7],
        'user_id': domain_raw[8],
    }

def parse_account(raw):
    return {
        'id': raw[0],
        'created': raw[1],
        'customer_id': raw[2],
        'subscription_type': raw[3],
        'user_id': raw[4],
        'client_reference_id': raw[5],
    }