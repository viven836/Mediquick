import mysql.connector

conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='mediquick'
    )
cursor = conn.cursor(buffered=True)