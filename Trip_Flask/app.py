import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'super_secret_key_tripconnect'

def get_db_connection():
    try:
        con = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'abhay@6263'),
            database=os.getenv('DB_NAME', 'trip'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        return con
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Static / Template Routing

@app.route('/')
@app.route('/index.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/signin.html')
def signin_page():
    return render_template('signin.html')

@app.route('/forgot.html')
def forgot_page():
    return render_template('forgot.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/buses.html')
@app.route('/busindex.html')
def buses_page():
    return render_template('busindex.html')

@app.route('/cars.html')
def cars_page():
    return render_template('cars.html')

@app.route('/mybooking.html')
def mybooking_page():
    return render_template('mybooking.html')

@app.route('/busForm')
def bus_form_page():
    return render_template('busForm.html')

@app.route('/first')
def first_page():
    # Clear session if logout behavior is desired
    session.clear()
    return render_template('first.html')

# AUTH PORTION

@app.route('/Ureg', methods=['POST'])
def ureg():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            q = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(q, (name, email, password))
            con.commit()
            # Equivalent to JS window.alert('Successfully Registration')
            # Assuming flash messages are somewhat shown or user just redirects
            # For exact parity, you could return JS alert, but redirect is cleaner.
            return "<script>window.alert('Successful Registration'); window.location.href='/login.html';</script>"
        except Exception as e:
            return f"<script>window.alert('Something Went Wrong: {e}'); window.location.href='/login.html';</script>"
        finally:
            cursor.close()
            con.close()
    return "DB Error"

@app.route('/Ulog', methods=['POST'])
def ulog():
    email = request.form.get('email')
    password = request.form.get('password')
    
    con = get_db_connection()
    if con:
        cursor = con.cursor(dictionary=True)
        try:
            q = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(q, (email, password))
            user = cursor.fetchone()
            if user:
                session['email'] = email
                session['user_id'] = user.get('id', '')
                return "<script>alert('Successfully Logged In!'); window.location.href='/dashboard.html';</script>"
            else:
                return "<script>alert('Invalid Email or Password'); window.location.href='/login.html';</script>"
        except Exception as e:
            return f"<h3>Database Error: {e}</h3>"
        finally:
            cursor.close()
            con.close()
    return "DB Error"

@app.route('/SendOTP', methods=['POST'])
def send_otp():
    email = request.form.get('email')
    import random
    otp = str(random.randint(1000, 9999))
    session['otp'] = otp
    session['email'] = email
    # Usually you'd send an email here.
    print(f"OTP for {email} is {otp}")
    return render_template('verifyOtp.html', email=email)

@app.route('/VerifyOTP', methods=['POST'])
def verify_otp():
    user_otp = request.form.get('otp')
    new_password = request.form.get('password')
    sys_otp = session.get('otp')
    email = session.get('email')
    
    if str(user_otp) == str(sys_otp):
        con = get_db_connection()
        if con:
            cursor = con.cursor()
            try:
                q = "UPDATE users SET password=%s WHERE email=%s"
                cursor.execute(q, (new_password, email))
                con.commit()
                return "<script>alert('Password Reset Successfully!'); window.location.href='/login.html';</script>"
            finally:
                cursor.close()
                con.close()
    else:
        return "<script>alert('Invalid OTP!'); window.location.href='/forgot.html';</script>"

# BUS BOOKING

@app.route('/SearchBus', methods=['POST'])
def search_bus():
    from_city = request.form.get('from')
    to_city = request.form.get('to')
    date = request.form.get('date')
    
    con = get_db_connection()
    buses = []
    if con:
        cursor = con.cursor(dictionary=False) # return list/tuple
        try:
            query = "SELECT * FROM buses WHERE LOWER(from_city)=LOWER(%s) AND LOWER(to_city)=LOWER(%s) AND seats_available > 0"
            cursor.execute(query, (from_city, to_city))
            results = cursor.fetchall()
            # Format buses to match JSP expectancy (ArrayList of String[])
            # Assuming DB cols: id(0), name(1), from(2), to(3), date(4), seats(5), type(6), arr_time(7), dep_time(8), price(9)
            # Make sure all are converted to string for parity w/ template.
            for row in results:
                buses.append([str(x) for x in row])
        finally:
            cursor.close()
            con.close()
            
    return render_template('busList.html', buses=buses)

@app.route('/BusBooking', methods=['POST'])
def bus_booking():
    bus_id = request.form.get('busId')
    fullname = request.form.get('fullname')
    mobile = request.form.get('mobile')
    passengers = int(request.form.get('passengers', 1))
    
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
            checkQuery = "SELECT seats_available FROM buses WHERE id=%s"
            cursor.execute(checkQuery, (bus_id,))
            res = cursor.fetchone()
            if res and res[0] >= passengers:
                insertQuery = "INSERT INTO busbookings (name, mobile, bus_id, passengers, status) VALUES (%s, %s, %s, %s, 'CONFIRMED')"
                # JS app might not have had status column here, adjust if needed
                # we'll assume it exists or falls back
                try:
                    cursor.execute(insertQuery, (fullname, mobile, bus_id, passengers))
                except mysql.connector.errors.ProgrammingError as e:
                    # fallback if status doesn't exist
                    insertQuery = "INSERT INTO busbookings (name, mobile, bus_id, passengers) VALUES (%s, %s, %s, %s)"
                    cursor.execute(insertQuery, (fullname, mobile, bus_id, passengers))
                
                updateQuery = "UPDATE buses SET seats_available = seats_available - %s WHERE id=%s AND seats_available >= %s"
                cursor.execute(updateQuery, (passengers, bus_id, passengers))
                con.commit()
                return "<script>alert('Bus Booking Confirmed!'); window.location.href='/mybooking.html';</script>"
            else:
                return "<script>alert('Not Enough Seats Available!'); window.location.href='/buses.html';</script>"
        except Exception as e:
             return f"<script>alert('Error: {e}'); window.location.href='/buses.html';</script>"
        finally:
            cursor.close()
            con.close()
            
@app.route('/CancelBooking', methods=['POST'])
def cancel_bus_booking():
    booking_id = request.form.get('cancel_id')
    
    con = get_db_connection()
    if con:
         # Need to fetch passengers and bus_id first, then cancel
         cursor = con.cursor()
         try:
             # Just an approximation: The java servlet does UPDATE busbookings... and UPDATE buses setup here
             cursor.execute("SELECT bus_id, passengers FROM busbookings WHERE id=%s AND status!='CANCELLED'", (booking_id,))
             res = cursor.fetchone()
             if res:
                 bus_id, passengers = res
                 cursor.execute("UPDATE busbookings SET status='CANCELLED' WHERE id=%s", (booking_id,))
                 cursor.execute("UPDATE buses SET seats_available = seats_available + %s WHERE id=%s", (passengers, bus_id))
                 con.commit()
             return redirect(url_for('view_bookings', mobile=request.form.get('mobile_no', '')))
         finally:
             cursor.close()
             con.close()

# CARS

@app.route('/SearchCar', methods=['POST'])
def search_car():
    city = request.form.get('city')
    con = get_db_connection()
    cars = []
    if con:
        cursor = con.cursor()
        try:
            query = "SELECT * FROM cars WHERE city=%s AND available > 0"
            cursor.execute(query, (city,))
            results = cursor.fetchall()
            for row in results:
                # 0: id, 1: name, 2: type, 3: price, 4: seats, 5: city
                cars.append([str(x) for x in row])
        finally:
            cursor.close()
            con.close()
    return render_template('carList.html', cars=cars)

@app.route('/CarBooking', methods=['POST'])
def car_booking():
    car_id = request.form.get('carId')
    price = float(request.form.get('price'))
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    days = int(request.form.get('days'))
    total_amount = days * price
    
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        try:
             query = "INSERT INTO carbookings (name, mobile, car_id, days, total_amount, status) VALUES (%s, %s, %s, %s, %s, 'CONFIRMED')"
             cursor.execute(query, (name, mobile, car_id, days, total_amount))
             
             update = "UPDATE cars SET available = available - 1 WHERE id=%s AND available > 0"
             cursor.execute(update, (car_id,))
             con.commit()
             return "<script>alert('Car Booking Confirmed!'); window.location.href='/mybooking.html';</script>"
        finally:
             cursor.close()
             con.close()
             
@app.route('/CancelCarBooking', methods=['POST'])
def cancel_car_booking():
    # Similar to others
    booking_id = request.form.get('cancel_id')
    con = get_db_connection()
    if con:
         cursor = con.cursor()
         try:
             cursor.execute("SELECT car_id FROM carbookings WHERE id=%s AND status!='CANCELLED'", (booking_id,))
             res = cursor.fetchone()
             if res:
                  car_id = res[0]
                  cursor.execute("UPDATE carbookings SET status='CANCELLED' WHERE id=%s", (booking_id,))
                  cursor.execute("UPDATE cars SET available = available + 1 WHERE id=%s", (car_id,))
                  con.commit()
             # usually returning back to view bookings
             # Not perfectly identical to the JSP form since it might need POST data.
             # We can just redirect to mybooking.
             return redirect(url_for('mybooking_page'))
         finally:
             cursor.close()
             con.close()

# HOTELS

@app.route('/hotels', methods=['GET', 'POST'])
@app.route('/hotels.html', methods=['GET', 'POST'])
def hotels_page():
    con = get_db_connection()
    hotels = []
    if con:
         cursor = con.cursor(dictionary=True)
         try:
              cursor.execute("SELECT * FROM hotels")
              hotels = cursor.fetchall()
         finally:
              cursor.close()
              con.close()
              
    selected_hotel = request.args.get('hotel', '')
    return render_template('hotels.html', hotels=hotels, selected_hotel=selected_hotel)

@app.route('/HotelSearch', methods=['POST'])
def search_hotel():
    location = request.form.get('location')
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')
    guests = request.form.get('guests')
    
    con = get_db_connection()
    hotels = []
    if con:
         cursor = con.cursor(dictionary=True)
         try:
              q = "SELECT * FROM hotels WHERE LOWER(location) LIKE LOWER(%s) AND max_guests >= %s"
              # Like operator with wildcard
              cursor.execute(q, (f"%{location}%", guests))
              hotels = cursor.fetchall()
         finally:
              cursor.close()
              con.close()
              
    # Hotels page expects hotels list. Re-rendering hotels.html with filtered list.
    return render_template('hotels.html', hotels=hotels)

@app.route('/HotelBooking', methods=['POST'])
def hotel_booking():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    hotelName = request.form.get('hotelName')
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')
    
    # Calculate days
    from datetime import datetime
    d1 = datetime.strptime(checkin, "%Y-%m-%d")
    d2 = datetime.strptime(checkout, "%Y-%m-%d")
    days = (d2 - d1).days
    
    con = get_db_connection()
    if con:
        cursor = con.cursor(dictionary=True)
        try:
            cursor.execute("SELECT price_per_night FROM hotels WHERE name = %s", (hotelName,))
            hotel = cursor.fetchone()
            if hotel:
                total_amount = days * hotel['price_per_night']
                query = "INSERT INTO bookings (fullname, email, mobile, hotel_name, checkin, checkout, days, total_amount, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'CONFIRMED')"
                cursor.execute(query, (fullname, email, mobile, hotelName, checkin, checkout, days, total_amount))
                con.commit()
                return "<script>alert('Hotel Booked Successfully!'); window.location.href='/mybooking.html';</script>"
        finally:
            cursor.close()
            con.close()
    return "Error"

@app.route('/CancelHotelBooking', methods=['POST'])
def cancel_hotel_booking():
    booking_id = request.form.get('cancel_id')
    con = get_db_connection()
    if con:
         cursor = con.cursor()
         try:
              query = "UPDATE bookings SET status='CANCELLED' WHERE id=%s"
              cursor.execute(query, (booking_id,))
              con.commit()
         finally:
              cursor.close()
              con.close()
    return redirect(url_for('mybooking_page'))


# VIEW BOOKINGS

@app.route('/ViewBookings', methods=['POST', 'GET'])
def view_bookings():
    mobile = request.values.get('mobile_no') or request.values.get('mobile')
    if not mobile:
         return redirect(url_for('mybooking_page'))
         
    # Need to fetch from busbookings, bookings (hotels), and carbookings
    history = []
    con = get_db_connection()
    if con:
         cursor = con.cursor(dictionary=True)
         try:
              # Fetch Buses
              busQuery = """SELECT b.id, bs.bus_name as service, bs.from_city as from_loc, bs.to_city as to_loc, bs.travel_date as date_val, b.passengers as qty, b.status 
                            FROM busbookings b JOIN buses bs ON b.bus_id = bs.id 
                            WHERE b.mobile=%s"""
              cursor.execute(busQuery, (mobile,))
              for r in cursor.fetchall():
                   r['type'] = 'Bus'
                   r['action'] = '/CancelBooking'
                   history.append(r)
                   
              # Fetch Hotels
              hotelQuery = """SELECT id, hotel_name as service, '' as from_loc, '' as to_loc, checkin as date_val, days as qty, status 
                              FROM bookings WHERE mobile=%s"""
              cursor.execute(hotelQuery, (mobile,))
              for r in cursor.fetchall():
                   r['type'] = 'Hotel'
                   r['action'] = '/CancelHotelBooking'
                   history.append(r)

              # Fetch Cars
              carQuery = """SELECT cb.id, c.car_name as service, c.city as from_loc, '' as to_loc, '' as date_val, cb.days as qty, cb.status
                            FROM carbookings cb JOIN cars c ON cb.car_id = c.id
                            WHERE cb.mobile=%s"""
              cursor.execute(carQuery, (mobile,))
              for r in cursor.fetchall():
                   r['type'] = 'Car'
                   r['action'] = '/CancelCarBooking'
                   history.append(r)
                   
         finally:
              cursor.close()
              con.close()
              
    return render_template('bookingHistory.html', history=history, mobile=mobile)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
