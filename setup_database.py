import mysql.connector
import os
import random
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
        
        # 2. Recreate Database
        print(f"Dropping and recreating database '{DB_NAME}'...")
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        
        # 3. Define Schemas
        tables = {
            'users': "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255) UNIQUE, password VARCHAR(255))",
            'buses': """
                CREATE TABLE buses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    bus_name VARCHAR(255),
                    from_city VARCHAR(255),
                    to_city VARCHAR(255),
                    travel_date DATE,
                    seats_available INT DEFAULT 40,
                    type VARCHAR(50),
                    arr_time TIME,
                    dep_time TIME,
                    price INT,
                    image VARCHAR(512)
                )
            """,
            'busbookings': "CREATE TABLE busbookings (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), mobile VARCHAR(20), bus_id INT, passengers INT, status VARCHAR(50) DEFAULT 'CONFIRMED', FOREIGN KEY (bus_id) REFERENCES buses(id))",
            'cars': "CREATE TABLE cars (id INT AUTO_INCREMENT PRIMARY KEY, car_name VARCHAR(255), type VARCHAR(50), price INT, seats INT, city VARCHAR(255), available INT, image VARCHAR(512))",
            'carbookings': "CREATE TABLE carbookings (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), mobile VARCHAR(20), car_id INT, days INT, total_amount DECIMAL(10,2), status VARCHAR(50) DEFAULT 'CONFIRMED', FOREIGN KEY (car_id) REFERENCES cars(id))",
            'hotels': "CREATE TABLE hotels (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), location VARCHAR(255), price_per_night INT, max_guests INT, description TEXT, rating DECIMAL(2,1), image VARCHAR(512))",
            'bookings': "CREATE TABLE bookings (id INT AUTO_INCREMENT PRIMARY KEY, fullname VARCHAR(255), email VARCHAR(255), mobile VARCHAR(20), hotel_name VARCHAR(255), checkin DATE, checkout DATE, days INT, total_amount DECIMAL(10,2), status VARCHAR(50) DEFAULT 'CONFIRMED')"
        }
        
        for name, schema in tables.items():
            cursor.execute(schema)
            
        # 4. Data Generation
        print("Generating algorithmic sample data...")
        
        # Constants
        HUBS = ['Mumbai', 'Pune', 'Delhi', 'Bangalore', 'Hyderabad']
        OTHER_CITIES = ['Goa', 'Jaipur', 'Ahmedabad', 'Indore', 'Bhopal', 'Surat', 'Chandigarh', 'Chennai', 'Pondicherry', 'Kolkata', 'Siliguri', 'Mysore', 'Nagpur', 'Lonavala']
        ALL_CITIES = HUBS + OTHER_CITIES
        
        BUS_OPERATORS = ['Shivneri', 'Neeta Travels', 'VRL Travels', 'Zingbus', 'Orange Travels', 'National Travels', 'SRS Travels', 'Jabbar Travels']
        BUS_TYPES = ['AC Sleeper', 'Premium AC', 'Semi-Sleeper', 'Volvo Multi-Axle', 'Electric AC']
        BUS_IMAGES = [
            'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?q=80&w=1000&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1570125909232-eb263c188f7e?q=80&w=1000&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1517030330234-94c4fa948ebc?q=80&w=1000&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1494515843206-f3117d3f51b7?q=80&w=1000&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1562620644-8585038c5bb4?q=80&w=1000&auto=format&fit=crop'
        ]

        today = datetime.now().date()
        bus_data = []

        # Generate Routes: Hub to All, All to Hub
        for hub in HUBS:
            for city in ALL_CITIES:
                if hub == city: continue
                
                # Bi-directional
                routes = [(hub, city), (city, hub)]
                
                for f, t in routes:
                    # 2 dates for each route (Today, Tomorrow)
                    for d_offset in range(3):
                        travel_date = today + timedelta(days=d_offset)
                        
                        # 2 buses per day (Morning/Evening)
                        # Morning
                        bus_data.append((
                            random.choice(BUS_OPERATORS), f, t, travel_date, random.randint(20, 45),
                            random.choice(BUS_TYPES), '06:00:00', '18:00:00', random.randint(500, 2500),
                            random.choice(BUS_IMAGES)
                        ))
                        # Evening
                        bus_data.append((
                            random.choice(BUS_OPERATORS) + " Express", f, t, travel_date, random.randint(20, 45),
                            random.choice(BUS_TYPES), '20:00:00', '08:00:00', random.randint(500, 2500),
                            random.choice(BUS_IMAGES)
                        ))

        cursor.executemany("INSERT INTO buses (bus_name, from_city, to_city, travel_date, seats_available, type, dep_time, arr_time, price, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", bus_data)
        print(f"Total Buses Seeded: {len(bus_data)}")

        # --- CARS --- (1 per city)
        car_data = []
        CAR_MODELS = [('Swift Dzire', 'Sedan', 2000), ('Thar 4x4', 'SUV', 5500), ('Fortuner', 'SUV', 6000), ('Honda City', 'Sedan', 2500), ('Mercedes C-Class', 'Luxury', 12000)]
        CAR_IMAGES = ['https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?q=80&w=800', 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?q=80&w=800', 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?q=80&w=800']
        
        for city in ALL_CITIES:
            model = random.choice(CAR_MODELS)
            car_data.append((model[0], model[1], model[2], 5, city, 3, random.choice(CAR_IMAGES)))
        
        cursor.executemany("INSERT INTO cars (car_name, type, price, seats, city, available, image) VALUES (%s, %s, %s, %s, %s, %s, %s)", car_data)

        # --- HOTELS --- (1-2 per city)
        hotel_data = []
        HOTEL_NAMES = ['JW Marriott', 'Taj Palace', 'Oberoi Grand', 'Novotel Resort', 'Leela Palace', 'ITC Grand', 'The Park']
        HOTEL_IMAGES = ['https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=1000', 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=1000']
        
        for city in ALL_CITIES:
            hotel_data.append((random.choice(HOTEL_NAMES) + " " + city, city, random.randint(4000, 20000), 2, "Luxury stay in " + city, 4.5, random.choice(HOTEL_IMAGES)))
            
        cursor.executemany("INSERT INTO hotels (name, location, price_per_night, max_guests, description, rating, image) VALUES (%s, %s, %s, %s, %s, %s, %s)", hotel_data)

        conn.commit()
        print("Seeding completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
