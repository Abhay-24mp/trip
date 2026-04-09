import mysql.connector
import os

def check_db():
    try:
        con = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'abhay@6263'),
            database=os.getenv('DB_NAME', 'trip'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT id, name, image FROM hotels")
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row['id']}, Name: {row['name']}, Image: {row['image']}")
        cursor.close()
        con.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db()
