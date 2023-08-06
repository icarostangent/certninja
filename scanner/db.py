import mysql.connector
import os
import uuid
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy import insert

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
database = os.environ.get('DB_DATABASE')


def insert(scan_object):
    try:
        print(f'[*] connecting to db {datetime.now()}')
        engine = create_engine(
            f"mysql://{user}:{password}@{host}/{database}", echo=True)
    except Exception as ex:
        print(f'[!] {ex}')
        exit(1)

    # insert_scan = (
    #     """INSERT INTO api_scan (
    #         user,
    #         domain,
    #         name,
    #         created,
    #         last_scan
    #     )
    #     VALUES (
    #         :user,
    #         :domain,
    #         :name,
    #         :created,
    #         :last_scan
    #     )"""
    # )

    # data = {
    #     'user': scan_object['user_id'],
    #     'domain': scan_object['domain'],
    #     'name': uuid.uuid4(),
    #     'created': datetime.now(),
    #     'last_scan': scan_object['output']
    # }

    # print(f'[*] creating insert statement {datetime.now()}')
    # stmt = (
    #     insert('api_scan').
    #     values(user_id=scan_object['user_id'], domain_id=scan_object['domain'], last_scan=scan_object['output'])
    # )

    print(f'[*] executing insert statement {datetime.now()}')
    with engine.connect() as conn:
        conn.execute(
            text(f"insert into api_scan SET user_id=:user_id, domain_id=:domain_id, uuid=:uuid, output=:output, created=:created"),
            {
                "user_id": scan_object['user_id'], 
                "domain_id": scan_object['domain_id'], 
                "uuid": str(uuid.uuid4()), 
                "output": scan_object['output'], 
                "created": datetime.now()
            }
        )

    print(f'[*] executing update statement {datetime.now()}')
    with engine.connect() as conn:
        conn.execute(
            text(f"UPDATE api_domain SET last_scan=:last_scan, scan_status=:status, modified=:now WHERE id=:id"),
            {
                "last_scan": scan_object['output'], 
                "status": "complete", 
                "now": datetime.now(), 
                "id": scan_object['domain_id']
            }
        )

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