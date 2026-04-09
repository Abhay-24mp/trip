import mysql.connector
import os

def check_all_images():
    try:
        con = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'abhay@6263'),
            database=os.getenv('DB_NAME', 'trip'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        cursor = con.cursor(dictionary=True)
        
        print("--- HOTELS ---")
        cursor.execute("SELECT id, name, image FROM hotels WHERE image LIKE '%1551882547%'")
        for row in cursor.fetchall():
            print(f"ID: {row['id']}, Name: {row['name']}, Image: {row['image']}")
            
        print("\n--- CARS ---")
        cursor.execute("SELECT id, car_name, image FROM cars WHERE image LIKE '%1551882547%'")
        for row in cursor.fetchall():
            print(f"ID: {row['id']}, Name: {row['car_name']}, Image: {row['image']}")
            
        print("\n--- BUSES ---")
        cursor.execute("SELECT id, bus_name, image FROM buses WHERE image LIKE '%1551882547%'")
        for row in cursor.fetchall():
            print(f"ID: {row['id']}, Name: {row['bus_name']}, Image: {row['image']}")
            
        cursor.close()
        con.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_all_images()
