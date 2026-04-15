import os
import mysql.connector

def get_db_connection():
    try:
        # Build connection args
        conn_args = dict(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'abhay@6263'),
            database=os.getenv('DB_NAME', 'trip'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        # Enable SSL if running in cloud (DB_HOST env var is set)
        if os.getenv('DB_HOST'):
            conn_args['ssl_disabled'] = False
            conn_args['ssl_verify_cert'] = False
            conn_args['ssl_verify_identity'] = False
        con = mysql.connector.connect(**conn_args)
        return con
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
