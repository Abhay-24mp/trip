import mysql.connector
import os

def update_images():
    try:
        con = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'abhay@6263'),
            database=os.getenv('DB_NAME', 'trip'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        cursor = con.cursor()
        
        # New working image URL
        new_url = "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?ixlib=rb-4.0.3&w=1080&fit=crop&q=80&fm=jpg"
        
        query = "UPDATE hotels SET image = %s WHERE image LIKE '%1551882547%'"
        cursor.execute(query, (new_url,))
        
        con.commit()
        print(f"Updated {cursor.rowcount} rows in hotels table.")
        
        cursor.close()
        con.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_images()
