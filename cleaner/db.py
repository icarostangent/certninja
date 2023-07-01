import mysql.connector
import os
import uuid
from datetime import datetime, timedelta

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
database = os.environ.get('DB_DATABASE')



# def get_domains():
#     try:
#         print('[*] connecting to db')
#         cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
#     except Exception as ex:
#         print(ex)
#         exit(1)

#     cursor = cnx.cursor()

#     stmt = "DELETE FROM wp_posts WHERE post_type = 'scan' and post_author='{}' and date_modified "

#     cursor.execute(stmt)

#     domains = [parse_domain(domain) for domain in cursor.fetchall()]

#     cursor.close()
#     cnx.close()

#     return domains

def clean(user_id, role):
    print(f'[+] Cleaning {user_id} {role}')
    try:
        # print('[*] connecting to db')
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    except Exception as ex:
        print(ex)
        exit(1)

    cursor = cnx.cursor()

    if 'starter' in role:
        stmt = f"delete from wp_posts where post_type='scan' and post_author='{user_id}' and post_modified < now() - interval 1 DAY;"
    
    elif 'basic' in role:
        stmt = f"delete from wp_posts where post_type='scan' and post_author='{user_id}' and post_modified < now() - interval 1 WEEK;"
    
    elif 'growth' in role:
        stmt = f"delete from wp_posts where post_type='scan' and post_author='{user_id}' and post_modified < now() - interval 3 MONTH;"
    
    elif 'ultimate' in role:
        stmt = f"delete from wp_posts where post_type='scan' and post_author='{user_id}' and post_modified < now() - interval 6 MONTH;"

    else:
        print("[!] Uknown role, aborting.")
    

    cursor.execute(stmt)

    domains = [parse_domain(domain) for domain in cursor.fetchall()]

    cursor.close()
    cnx.close()