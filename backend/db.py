import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='flaskuser',
        password=os.environ.get('DB_PASSWORD'),
        database='mediquick'
    )
