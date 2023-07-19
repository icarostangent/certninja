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

def get_user_role(id):
    try:
        # print('[*] connecting to db')
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    except Exception as ex:
        print(ex)
        exit(1)

    cursor = cnx.cursor()
    stmt = "select * from wp_usermeta where meta_key = 'wp_capabilities'"
    cursor.execute(stmt)
    users = [user for user in cursor.fetchall()]
    usermeta = [user for user in users if user[1] == id].pop()

    cursor.close()
    cnx.close()

    return parse_usermeta(usermeta)['meta_value']

def set_scan_status(status, id):
    try:
        # print('[*] connecting to db')
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    except Exception as ex:
        print(ex)
        exit(1)

    cursor = cnx.cursor()
    stmt = f"UPDATE wp_posts SET post_content_filtered = '{status}' WHERE id = '{id}'"
    cursor.execute(stmt)
    cnx.commit()
    cursor.close()
    cnx.close()


def parse_domain(domain_raw):
    return {
        'id': domain_raw[0],
        'name': domain_raw[1],
        'ip_address': domain_raw[2],
        'port': domain_raw[3],
        'last_scan': domain_raw[4],
        'user_id': domain_raw[5],
        'scan_status': domain_raw[6],
        'created': domain_raw[7],
        'modified': domain_raw[8],
    }

def parse_usermeta(raw):
    return {
        'umeta_id': raw[0],
        'user_id': raw[1],
        'meta_key': raw[2],
        'meta_value': raw[3],
    }