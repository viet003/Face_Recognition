import mysql.connector

def connect_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Viet211003@s',
            database='facereg'
        )
        
        if connection.is_connected():
            return connection

    except Error as e:
        print("Lỗi khi kết nối đến MySQL:", e)
        return None
