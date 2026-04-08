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
        
        # 2. Create Database
        print(f"Creating database '{DB_NAME}' if it doesn't exist...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        
        # 3. Define Schemas
        tables = {
            'users': """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                )
            """,
            'buses': """
                CREATE TABLE IF NOT EXISTS buses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    bus_name VARCHAR(255) NOT NULL,
                    from_city VARCHAR(255) NOT NULL,
                    to_city VARCHAR(255) NOT NULL,
                    travel_date DATE NOT NULL,
                    seats_available INT DEFAULT 40,
                    type VARCHAR(50),
                    arr_time TIME,
                    dep_time TIME,
                    price DECIMAL(10, 2)
                )
            """,
            'busbookings': """
                CREATE TABLE IF NOT EXISTS busbookings (
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
                CREATE TABLE IF NOT EXISTS cars (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    car_name VARCHAR(255) NOT NULL,
                    type VARCHAR(50),
                    price DECIMAL(10, 2),
                    seats INT,
                    city VARCHAR(255),
                    available INT DEFAULT 1
                )
            """,
            'carbookings': """
                CREATE TABLE IF NOT EXISTS carbookings (
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
                CREATE TABLE IF NOT EXISTS hotels (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    price_per_night DECIMAL(10, 2),
                    max_guests INT DEFAULT 2,
                    description TEXT,
                    rating DECIMAL(2, 1) DEFAULT 4.0
                )
            """,
            'bookings': """
                CREATE TABLE IF NOT EXISTS bookings (
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
        print("Seeding sample data...")
        
        # Sample Buses
        cursor.execute("SELECT COUNT(*) FROM buses")
        if cursor.fetchone()[0] == 0:
            today = datetime.now().date()
            bus_data = [
                ('Shivneri', 'Pune', 'Mumbai', today + timedelta(days=1), 40, 'AC Sleeper', '10:00:00', '14:00:00', 550.00),
                ('Neeta Travels', 'Mumbai', 'Pune', today + timedelta(days=1), 35, 'Non-AC', '08:00:00', '11:00:00', 400.00),
                ('Purple Travels', 'Pune', 'Delhi', today + timedelta(days=2), 40, 'AC Seater', '18:00:00', '10:00:00', 2500.00)
            ]
            cursor.executemany("INSERT INTO buses (bus_name, from_city, to_city, travel_date, seats_available, type, arr_time, dep_time, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", bus_data)

        # Sample Cars
        cursor.execute("SELECT COUNT(*) FROM cars")
        if cursor.fetchone()[0] == 0:
            car_data = [
                ('Swift Dzire', 'Sedan', 2000.00, 4, 'Pune', 5),
                ('Innova Crysta', 'SUV', 4500.00, 7, 'Mumbai', 3),
                ('Honda City', 'Sedan', 2500.00, 4, 'Delhi', 4)
            ]
            cursor.executemany("INSERT INTO cars (car_name, type, price, seats, city, available) VALUES (%s, %s, %s, %s, %s, %s)", car_data)

        # Sample Hotels
        cursor.execute("SELECT COUNT(*) FROM hotels")
        if cursor.fetchone()[0] == 0:
            hotel_data = [
                ('JW Marriott', 'Pune', 8500.00, 2, 'Luxury stay in the heart of Pune', 4.8),
                ('Taj Lands End', 'Mumbai', 15000.00, 2, 'Iconic luxury hotel with sea view', 4.9),
                ('The Oberoi', 'Delhi', 12000.00, 2, 'Fine dining and premium rooms', 4.7)
            ]
            cursor.executemany("INSERT INTO hotels (name, location, price_per_night, max_guests, description, rating) VALUES (%s, %s, %s, %s, %s, %s)", hotel_data)

        conn.commit()
        print("\nDatabase setup completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
