from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from functools import wraps
from database import get_db_connection
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_email' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Admin credentials as requested
        if email == 'abhaypawarmp@gmail.com' and password == 'abhay123456':
            session['admin_email'] = email
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin/login.html', error='Invalid admin credentials')
            
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_email', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    con = get_db_connection()
    stats = {}
    recent_bookings = []
    if con:
        cursor = con.cursor(dictionary=True)
        try:
            # Stats
            cursor.execute("SELECT COUNT(*) as count FROM bookings")
            hotel_bookings = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM busbookings")
            bus_bookings = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM carbookings")
            car_bookings = cursor.fetchone()['count']
            
            stats['total_bookings'] = hotel_bookings + bus_bookings + car_bookings
            
            # Revenue calculation
            cursor.execute("SELECT SUM(total_amount) as total FROM bookings WHERE status='CONFIRMED'")
            hotel_rev = cursor.fetchone()['total'] or 0
            
            # Note: busbookings and carbookings schema check needed for revenue
            # Assuming busbookings might not have total_amount, we might need to calculate or check actual schema
            # carbookings has total_amount
            cursor.execute("SELECT SUM(total_amount) as total FROM carbookings WHERE status='CONFIRMED'")
            car_rev = cursor.fetchone()['total'] or 0
            
            # For buses, if no total_amount, we use price * passengers from joins?
            # Let's check busbookings table again from app.py
            # Line 311: "INSERT INTO busbookings (name, mobile, bus_id, passengers, status) VALUES (%s, %s, %s, %s, 'CONFIRMED')"
            # No total_amount in busbookings! I should calculate it from buses table.
            cursor.execute("""
                SELECT SUM(bb.passengers * b.price) as total 
                FROM busbookings bb 
                JOIN buses b ON bb.bus_id = b.id 
                WHERE bb.status='CONFIRMED'
            """)
            bus_rev = cursor.fetchone()['total'] or 0
            
            stats['total_revenue'] = hotel_rev + car_rev + bus_rev
            
            cursor.execute("SELECT COUNT(*) as count FROM hotels")
            stats['total_hotels'] = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM buses")
            stats['total_buses'] = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM cars")
            stats['total_cars'] = cursor.fetchone()['count']

            # Recent Bookings
            cursor.execute("SELECT 'Hotel' as type, fullname as name, hotel_name as service, total_amount as amount, status FROM bookings ORDER BY id DESC LIMIT 5")
            hotel_list = cursor.fetchall()
            
            cursor.execute("""
                SELECT 'Bus' as type, bb.name, b.bus_name as service, (bb.passengers * b.price) as amount, bb.status 
                FROM busbookings bb JOIN buses b ON bb.bus_id = b.id ORDER BY bb.id DESC LIMIT 5
            """)
            bus_list = cursor.fetchall()
            
            cursor.execute("SELECT 'Car' as type, name, '' as service, total_amount as amount, status FROM carbookings ORDER BY id DESC LIMIT 5")
            car_list = cursor.fetchall()
            
            recent_bookings = hotel_list + bus_list + car_list
            recent_bookings.sort(key=lambda x: 1, reverse=True) # Needs better sorting if dates were available
            recent_bookings = recent_bookings[:10]

        finally:
            cursor.close()
            con.close()
            
    return render_template('admin/dashboard.html', active_page='dashboard', stats=stats, recent_bookings=recent_bookings)

# --- HOTEL MANAGEMENT ---

@admin_bp.route('/hotels')
@admin_required
def hotels():
    con = get_db_connection()
    hotels = []
    if con:
        cursor = con.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM hotels ORDER BY id DESC")
            hotels = cursor.fetchall()
        finally:
            cursor.close()
            con.close()
    return render_template('admin/hotels.html', active_page='hotels', hotels=hotels)

@admin_bp.route('/hotels/add', methods=['POST'])
@admin_required
def add_hotel():
    name = request.form.get('name')
    location = request.form.get('location')
    price = request.form.get('price_per_night')
    guests = request.form.get('max_guests')
    desc = request.form.get('description')
    image = request.form.get('image')
    
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            q = "INSERT INTO hotels (name, location, price_per_night, max_guests, description, image) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(q, (name, location, price, guests, desc, image))
            con.commit()
        finally:
            cursor.close()
            con.close()
    return redirect(url_for('admin.hotels'))

@admin_bp.route('/hotels/edit/<int:id>', methods=['POST'])
@admin_required
def edit_hotel(id):
    name = request.form.get('name')
    location = request.form.get('location')
    price = request.form.get('price_per_night')
    guests = request.form.get('max_guests')
    desc = request.form.get('description')
    image = request.form.get('image')
    
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            q = "UPDATE hotels SET name=%s, location=%s, price_per_night=%s, max_guests=%s, description=%s, image=%s WHERE id=%s"
            cursor.execute(q, (name, location, price, guests, desc, image, id))
            con.commit()
        finally:
            cursor.close()
            con.close()
    return redirect(url_for('admin.hotels'))

@admin_bp.route('/hotels/delete/<int:id>', methods=['POST'])
@admin_required
def delete_hotel(id):
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM hotels WHERE id=%s", (id,))
            con.commit()
        finally:
            cursor.close()
            con.close()
    return redirect(url_for('admin.hotels'))

# --- CAR MANAGEMENT ---

@admin_bp.route('/cars')
@admin_required
def cars():
    con = get_db_connection()
    cars = []
    if con:
        cursor = con.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM cars ORDER BY id DESC")
            cars = cursor.fetchall()
        finally:
            cursor.close()
            con.close()
    return render_template('admin/cars.html', active_page='cars', cars=cars)

@admin_bp.route('/cars/add', methods=['POST'])
@admin_required
def add_car():
    name = request.form.get('car_name')
    ctype = request.form.get('type')
    price = request.form.get('price')
    seats = request.form.get('seats')
    city = request.form.get('city')
    available = request.form.get('available')
    image = request.form.get('image')
    
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            q = "INSERT INTO cars (car_name, type, price, seats, city, available, image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(q, (name, ctype, price, seats, city, available, image))
            con.commit()
        finally:
            cursor.close()
            con.close()
    return redirect(url_for('admin.cars'))

@admin_bp.route('/cars/edit/<int:id>', methods=['POST'])
@admin_required
def edit_car(id):
    name = request.form.get('car_name')
    ctype = request.form.get('type')
    price = request.form.get('price')
    seats = request.form.get('seats')
    city = request.form.get('city')
    available = request.form.get('available')
    image = request.form.get('image')
    
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            q = "UPDATE cars SET car_name=%s, type=%s, price=%s, seats=%s, city=%s, available=%s, image=%s WHERE id=%s"
            cursor.execute(q, (name, ctype, price, seats, city, available, image, id))
            con.commit()
        finally:
            cursor.close()
            con.close()
    return redirect(url_for('admin.cars'))

@admin_bp.route('/cars/delete/<int:id>', methods=['POST'])
@admin_required
def delete_car(id):
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM cars WHERE id=%s", (id,))
            con.commit()
        finally:
            cursor.close()
            con.close()
    return redirect(url_for('admin.cars'))

# --- BUS MANAGEMENT ---

@admin_bp.route('/buses')
@admin_required
def buses():
    con = get_db_connection()
    buses = []
    if con:
        cursor = con.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM buses ORDER BY id DESC")
            buses = cursor.fetchall()
        finally:
            cursor.close()
            con.close()
    return render_template('admin/buses.html', active_page='buses', buses=buses)

@admin_bp.route('/buses/add', methods=['POST'])
@admin_required
def add_bus():
    name = request.form.get('bus_name')
    from_city = request.form.get('from_city')
    to_city = request.form.get('to_city')
    travel_date = request.form.get('travel_date')
    seats = request.form.get('seats_available')
    btype = request.form.get('type')
    arr = request.form.get('arr_time')
    dep = request.form.get('dep_time')
    price = request.form.get('price')
    image = request.form.get('image')
    
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            q = "INSERT INTO buses (bus_name, from_city, to_city, travel_date, seats_available, type, arr_time, dep_time, price, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(q, (name, from_city, to_city, travel_date, seats, btype, arr, dep, price, image))
            con.commit()
        finally:
            cursor.close()
            con.close()
    return redirect(url_for('admin.buses'))

@admin_bp.route('/buses/edit/<int:id>', methods=['POST'])
@admin_required
def edit_bus(id):
    name = request.form.get('bus_name')
    from_city = request.form.get('from_city')
    to_city = request.form.get('to_city')
    travel_date = request.form.get('travel_date')
    seats = request.form.get('seats_available')
    btype = request.form.get('type')
    arr = request.form.get('arr_time')
    dep = request.form.get('dep_time')
    price = request.form.get('price')
    image = request.form.get('image')
    
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            q = "UPDATE buses SET bus_name=%s, from_city=%s, to_city=%s, travel_date=%s, seats_available=%s, type=%s, arr_time=%s, dep_time=%s, price=%s, image=%s WHERE id=%s"
            cursor.execute(q, (name, from_city, to_city, travel_date, seats, btype, arr, dep, price, image, id))
            con.commit()
        finally:
            cursor.close()
            con.close()
    return redirect(url_for('admin.buses'))

@admin_bp.route('/buses/delete/<int:id>', methods=['POST'])
@admin_required
def delete_bus(id):
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM buses WHERE id=%s", (id,))
            con.commit()
        finally:
            cursor.close()
            con.close()
    return redirect(url_for('admin.buses'))

# --- BOOKING MANAGEMENT ---

@admin_bp.route('/bookings')
@admin_required
def bookings():
    service_type = request.args.get('type', 'all')
    search = request.args.get('search', '')
    
    con = get_db_connection()
    bookings_list = []
    
    if con:
        cursor = con.cursor(dictionary=True)
        try:
            # Hotel Bookings
            if service_type in ['all', 'hotel']:
                q = "SELECT id, 'hotel' as service_type, fullname as customer, email, mobile, hotel_name as service, status FROM bookings"
                if search:
                    q += " WHERE (fullname LIKE %s OR email LIKE %s OR mobile LIKE %s OR id LIKE %s)"
                    cursor.execute(q, (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
                else:
                    cursor.execute(q)
                bookings_list += cursor.fetchall()
            
            # Car Bookings
            if service_type in ['all', 'car']:
                q = "SELECT cb.id, 'car' as service_type, cb.name as customer, '' as email, cb.mobile, c.car_name as service, cb.status FROM carbookings cb JOIN cars c ON cb.car_id = c.id"
                if search:
                    q += " WHERE (cb.name LIKE %s OR cb.mobile LIKE %s OR cb.id LIKE %s)"
                    cursor.execute(q, (f"%{search}%", f"%{search}%", f"%{search}%"))
                else:
                    cursor.execute(q)
                bookings_list += cursor.fetchall()
                
            # Bus Bookings
            if service_type in ['all', 'bus']:
                q = "SELECT bb.id, 'bus' as service_type, bb.name as customer, '' as email, bb.mobile, b.bus_name as service, bb.status FROM busbookings bb JOIN buses b ON bb.bus_id = b.id"
                if search:
                    q += " WHERE (bb.name LIKE %s OR bb.mobile LIKE %s OR bb.id LIKE %s)"
                    cursor.execute(q, (f"%{search}%", f"%{search}%", f"%{search}%"))
                else:
                    cursor.execute(q)
                bookings_list += cursor.fetchall()
                
            # Sort by ID descending (approximate chronological order)
            bookings_list.sort(key=lambda x: x['id'], reverse=True)
            
        finally:
            cursor.close()
            con.close()
            
    return render_template('admin/bookings.html', active_page='bookings', bookings=bookings_list, service_type=service_type, search=search)

@admin_bp.route('/bookings/update/<string:stype>/<int:id>', methods=['POST'])
@admin_required
def update_booking_status(stype, id):
    new_status = request.form.get('status')
    
    table_map = {
        'hotel': 'bookings',
        'car': 'carbookings',
        'bus': 'busbookings'
    }
    
    table = table_map.get(stype)
    if not table:
        return redirect(url_for('admin.bookings'))
        
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            cursor.execute(f"UPDATE {table} SET status=%s WHERE id=%s", (new_status, id))
            con.commit()
        finally:
            cursor.close()
            con.close()
            
    return redirect(url_for('admin.bookings'))

