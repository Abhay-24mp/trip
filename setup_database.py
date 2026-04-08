import mysql.connector
import os
from datetime import datetime, timedelta

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'abhay@6263'),
    'port': int(os.getenv('DB_PORT', 3306))
}

DB_NAME = 'trip'

def setup_database():
    try:
        # 1. Connect to MySQL Server
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 2. Recreate Database to ensure clean slate
        print(f"Dropping and recreating database '{DB_NAME}'...")
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        
        # 3. Define Schemas aligned perfectly with app.py expectations
        tables = {
            'users': """
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                )
            """,
            'buses': """
                CREATE TABLE buses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    bus_name VARCHAR(255) NOT NULL,
                    from_city VARCHAR(255) NOT NULL,
                    to_city VARCHAR(255) NOT NULL,
                    travel_date DATE NOT NULL,
                    seats_available INT DEFAULT 40,
                    type VARCHAR(50),
                    arr_time TIME,
                    dep_time TIME,
                    price INT
                )
            """,
            'busbookings': """
                CREATE TABLE busbookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    mobile VARCHAR(20) NOT NULL,
                    bus_id INT,
                    passengers INT DEFAULT 1,
                    status VARCHAR(50) DEFAULT 'CONFIRMED',
                    FOREIGN KEY (bus_id) REFERENCES buses(id)
                )
            """,
            'cars': """
                CREATE TABLE cars (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    car_name VARCHAR(255) NOT NULL,
                    type VARCHAR(50),
                    price INT,
                    seats INT,
                    city VARCHAR(255),
                    available INT DEFAULT 5
                )
            """,
            'carbookings': """
                CREATE TABLE carbookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    mobile VARCHAR(20) NOT NULL,
                    car_id INT,
                    days INT DEFAULT 1,
                    total_amount DECIMAL(10, 2),
                    status VARCHAR(50) DEFAULT 'CONFIRMED',
                    FOREIGN KEY (car_id) REFERENCES cars(id)
                )
            """,
            'hotels': """
                CREATE TABLE hotels (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    price_per_night INT,
                    max_guests INT DEFAULT 2,
                    description TEXT,
                    rating DECIMAL(2, 1) DEFAULT 4.0
                )
            """,
            'bookings': """
                CREATE TABLE bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fullname VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    mobile VARCHAR(20) NOT NULL,
                    hotel_name VARCHAR(255),
                    checkin DATE,
                    checkout DATE,
                    days INT,
                    total_amount DECIMAL(10, 2),
                    status VARCHAR(50) DEFAULT 'CONFIRMED'
                )
            """
        }
        
        for table_name, schema in tables.items():
            print(f"Creating table '{table_name}'...")
            cursor.execute(schema)
            
        # 4. Insert Sample Data
        print("Seeding fresh sample data...")
        
        today = datetime.now().date()
        
        # Buses: (id, name, from, to, date, seats, type, arr, dep, price)
        bus_data = [
            ('Shivneri', 'Pune', 'Mumbai', today + timedelta(days=1), 40, 'AC Sleeper', '14:00:00', '10:00:00', 550),
            ('Neeta Travels', 'Mumbai', 'Pune', today + timedelta(days=1), 35, 'Semi-Luxury', '11:00:00', '08:00:00', 400),
            ('Purple Travels', 'Pune', 'Delhi', today + timedelta(days=2), 40, 'AC Seater', '10:00:00', '18:00:00', 2500)
        ]
        cursor.executemany("INSERT INTO buses (bus_name, from_city, to_city, travel_date, seats_available, type, arr_time, dep_time, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", bus_data)

        # Cars: (id, name, type, price, seats, city, available)
        car_data = [
            ('Swift Dzire', 'Sedan', 2000, 4, 'Pune', 5),
            ('Innova Crysta', 'SUV', 4500, 7, 'Mumbai', 3),
            ('Honda City', 'Sedan', 2500, 4, 'Delhi', 4)
        ]
        cursor.executemany("INSERT INTO cars (car_name, type, price, seats, city, available) VALUES (%s, %s, %s, %s, %s, %s)", car_data)

        # Hotels
        hotel_data = [
            ('JW Marriott', 'Pune', 8500, 2, 'Luxury stay in Pune', 4.8),
            ('Taj Lands End', 'Mumbai', 15000, 2, 'Sea view luxury', 4.9),
            ('The Oberoi', 'Delhi', 12000, 2, 'Premium hospitality', 4.7)
        ]
        cursor.executemany("INSERT INTO hotels (name, location, price_per_night, max_guests, description, rating) VALUES (%s, %s, %s, %s, %s, %s)", hotel_data)

        conn.commit()
        print("\nDatabase synchronization completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
