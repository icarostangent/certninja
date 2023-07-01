import mysql.connector
import os
import time
from datetime import date, datetime
from sqlalchemy import create_engine, text

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
database = os.environ.get('DB_DATABASE')


def run(scan_object):
    try:
        print(f'[*] scanner connecting to db {time.time()}')
        engine = create_engine(
            f"mysql://{user}:{password}@{host}/{database}", echo=True)
    except Exception as ex:
        print(f'[!] {ex}')
        exit(1)

    now = datetime.now()
    now_utc = now.utcnow()
    insert_scan_cpt = (
        """INSERT INTO wp_posts (
            post_author,
            post_date,
            post_date_gmt,
            post_content,
            post_title,
            post_excerpt,
            post_status,
            comment_status,
            ping_status,
            post_password,
            post_name,
            to_ping,
            pinged,
            post_modified,
            post_modified_gmt,
            post_content_filtered,
            post_parent,
            guid,
            menu_order,
            post_type,
            post_mime_type,
            comment_count
        )
        VALUES (
            :post_author,
            :post_date,
            :post_date_gmt,
            :post_content,
            :post_title,
            :post_excerpt,
            :post_status,
            :comment_status,
            :ping_status,
            :post_password,
            :post_name,
            :to_ping,
            :pinged,
            :post_modified,
            :post_modified_gmt,
            :post_content_filtered,
            :post_parent,
            :guid,
            :menu_order,
            :post_type,
            :post_mime_type,
            :comment_count
        )"""
    )

    data = {
        'post_author': scan_object['author_id'],  # author
        'post_date': now,
        'post_date_gmt': now_utc,
        'post_content': scan_object['output'],  # content
        'post_title': scan_object['domain_id'],  # title
        'post_excerpt': '',  # excerpt
        'post_status': 'publish',
        'comment_status': 'closed',
        'ping_status': 'closed',
        'post_password': '',
        # name
        'post_name': f"{scan_object['domain']}_{scan_object['ip']}_{now}",
        'to_ping': '',
        'pinged': '',
        'post_modified': now,
        'post_modified_gmt': now_utc,
        'post_content_filtered': '',  # content filtered
        'post_parent': 0,
        'guid': '',
        'menu_order': 0,
        'post_type': 'scan',
        'post_mime_type': '',
        'comment_count': 0
    }

    with engine.connect() as conn:
        conn.execute(
            text(insert_scan_cpt),
            data
        )

    with engine.connect() as conn:
        conn.execute(
            text(f"UPDATE wp_posts SET post_content=:output, post_content_filtered=:status, post_modified=:now, post_modified_gmt=:now_utc WHERE id=:id"),
            {"output": scan_object['output'], "status": "complete", "now": now, "now_utc": now_utc, "id": scan_object['domain_id']}
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