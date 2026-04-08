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
        
        # 3. Define Schemas
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
                    price INT,
                    image VARCHAR(512)
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
                    available INT DEFAULT 5,
                    image VARCHAR(512)
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
                    rating DECIMAL(2, 1) DEFAULT 4.0,
                    image VARCHAR(512)
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
            
        # 4. Insert Expanded Sample Data
        print("Seeding fresh sample data with images...")
        
        today = datetime.now().date()
        
        # --- BUSES ---
        bus_data = [
            ('Shivneri', 'Pune', 'Mumbai', today + timedelta(days=1), 40, 'AC Sleeper', '14:00:00', '10:00:00', 550, 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?q=80&w=2000&auto=format&fit=crop'),
            ('Neeta Travels', 'Mumbai', 'Pune', today + timedelta(days=1), 35, 'Semi-Luxury', '11:00:00', '08:00:00', 400, 'https://images.unsplash.com/photo-1570125909232-eb263c188f7e?q=80&w=2000&auto=format&fit=crop'),
            ('VRL Travels', 'Pune', 'Goa', today + timedelta(days=2), 40, 'Premium AC', '08:00:00', '22:00:00', 1200, 'https://images.unsplash.com/photo-1517030330234-94c4fa948ebc?q=80&w=1000&auto=format&fit=crop'),
            ('Zingbus', 'Delhi', 'Jaipur', today + timedelta(days=1), 45, 'Electric AC', '12:00:00', '06:00:00', 800, 'https://images.unsplash.com/photo-1494515843206-f3117d3f51b7?q=80&w=1000&auto=format&fit=crop'),
            ('Orange Travels', 'Bangalore', 'Hyderabad', today + timedelta(days=1), 30, 'Multi-Axle Sleeper', '09:00:00', '21:00:00', 1500, 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?q=80&w=2000&auto=format&fit=crop'),
            ('Jabbar Travels', 'Hyderabad', 'Bangalore', today + timedelta(days=3), 40, 'Sleeper', '07:00:00', '19:00:00', 1400, 'https://images.unsplash.com/photo-1562620644-8585038c5bb4?q=80&w=1000&auto=format&fit=crop')
        ]
        cursor.executemany("INSERT INTO buses (bus_name, from_city, to_city, travel_date, seats_available, type, arr_time, dep_time, price, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", bus_data)

        # --- CARS ---
        car_data = [
            ('Swift Dzire', 'Sedan', 2000, 4, 'Pune', 5, 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?q=80&w=800&auto=format&fit=crop'),
            ('Thar 4x4', 'SUV', 5500, 4, 'Goa', 3, 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?q=80&w=800&auto=format&fit=crop'),
            ('Innova Crysta', 'SUV', 4500, 7, 'Mumbai', 3, 'https://images.unsplash.com/photo-1562620644-8585038c5bb4?q=80&w=800&auto=format&fit=crop'),
            ('Honda City', 'Sedan', 2500, 4, 'Delhi', 4, 'https://images.unsplash.com/photo-1525609004556-c46c7d6cf048?q=80&w=800&auto=format&fit=crop'),
            ('Fortuner', 'SUV', 6000, 7, 'Delhi', 2, 'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?q=80&w=800&auto=format&fit=crop'),
            ('Mercedes C-Class', 'Luxury', 12000, 4, 'Mumbai', 2, 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?q=80&w=800&auto=format&fit=crop'),
            ('Baleno', 'Hatchback', 1800, 4, 'Bangalore', 6, 'https://images.unsplash.com/photo-1502877338535-766e1452684a?q=80&w=800&auto=format&fit=crop')
        ]
        cursor.executemany("INSERT INTO cars (car_name, type, price, seats, city, available, image) VALUES (%s, %s, %s, %s, %s, %s, %s)", car_data)

        # --- HOTELS ---
        hotel_data = [
            ('JW Marriott', 'Pune', 8500, 2, 'Luxury stay in the heart of the city.', 4.8, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=1000&auto=format&fit=crop'),
            ('Taj Lands End', 'Mumbai', 18000, 2, 'Legendary luxury with stunning sea views.', 4.9, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=1000&auto=format&fit=crop'),
            ('The Oberoi', 'Delhi', 14000, 2, 'Timeless elegance and world-class hospitality.', 4.7, 'https://images.unsplash.com/photo-1551882547-ff43c69e5cf2?q=80&w=1000&auto=format&fit=crop'),
            ('Novotel Resort', 'Goa', 7500, 3, 'Beachside bliss with family-friendly amenities.', 4.5, 'https://images.unsplash.com/photo-1571011299480-15296be4352d?q=80&w=1000&auto=format&fit=crop'),
            ('The Leela Palace', 'Bangalore', 16000, 2, 'Royal luxury amidst lush gardens.', 4.9, 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?q=80&w=1000&auto=format&fit=crop'),
            ('ITC Grand Chola', 'Chennai', 11000, 2, 'Architectural marvel with exceptional dining.', 4.6, 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?q=80&w=1000&auto=format&fit=crop'),
            ('ITC Rajputana', 'Jaipur', 9000, 2, 'Experience the royal heritage of Jaipur.', 4.5, 'https://images.unsplash.com/photo-1549412650-ef354fd4b154?q=80&w=1000&auto=format&fit=crop'),
            ('The Park', 'Hyderabad', 5500, 2, 'Contemporary luxury with a vibrant nightlife.', 4.3, 'https://images.unsplash.com/photo-1582719508461-905c673771fd?q=80&w=1000&auto=format&fit=crop')
        ]
        cursor.executemany("INSERT INTO hotels (name, location, price_per_night, max_guests, description, rating, image) VALUES (%s, %s, %s, %s, %s, %s, %s)", hotel_data)

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
