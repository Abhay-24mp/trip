import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from datetime import datetime
import razorpay

app = Flask(__name__)

RAZORPAY_KEY_ID = 'rzp_test_ScKVDGjGcqEnLD'
RAZORPAY_KEY_SECRET = '6HDINF3WzqpUX96uy3jtvzfX'
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
app.secret_key = 'super_secret_key_tripconnect'

def get_db_connection():
    try:
        # Build connection args
        conn_args = dict(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'abhay@6263'),
            database=os.getenv('DB_NAME', 'trip'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        # Enable SSL if running in cloud (DB_HOST env var is set)
        if os.getenv('DB_HOST'):
            conn_args['ssl_disabled'] = False
            conn_args['ssl_verify_cert'] = False
            conn_args['ssl_verify_identity'] = False
        con = mysql.connector.connect(**conn_args)
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
    if 'email' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html')

@app.route('/buses.html')
@app.route('/busindex.html')
def buses_page():
    if 'email' not in session:
        return redirect(url_for('login_page'))
    return render_template('busindex.html')

@app.route('/cars.html')
def cars_page():
    if 'email' not in session:
        return redirect(url_for('login_page'))
    con = get_db_connection()
    cities = []
    if con:
        cursor = con.cursor()
        try:
            cursor.execute("SELECT DISTINCT city FROM cars ORDER BY city")
            cities = [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            con.close()
    return render_template('cars.html', cities=cities)

@app.route('/mybooking.html')
def mybooking_page():
    if 'email' not in session:
        return redirect(url_for('login_page'))
    return render_template('mybooking.html')

@app.route('/busForm')
def bus_form_page():
    con = get_db_connection()
    from_cities = []
    to_cities = []
    if con:
        cursor = con.cursor()
        try:
            cursor.execute("SELECT DISTINCT from_city FROM buses ORDER BY from_city")
            from_cities = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT DISTINCT to_city FROM buses ORDER BY to_city")
            to_cities = [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            con.close()
    today = datetime.now().date().strftime('%Y-%m-%d')
    return render_template('busForm.html', from_cities=from_cities, to_cities=to_cities, today=today)

@app.route('/first')
def first_page():
    # Clear session if logout behavior is desired
    session.clear()
    return redirect(url_for('index'))

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
            return render_template('notification.html', 
                                   notif_type='success', 
                                   title='Registration Successful', 
                                   message='Your account has been created. Welcome to TripConnect!', 
                                   redirect_url='/login.html')
        except Exception as e:
            return render_template('notification.html', 
                                   notif_type='error', 
                                   title='Registration Failed', 
                                   message=f'Something went wrong: {e}', 
                                   redirect_url='/login.html')
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
                return render_template('notification.html', 
                                       notif_type='success', 
                                       title='Login Successful', 
                                       message=f'Welcome back, {user.get("name", "User")}!', 
                                       redirect_url='/dashboard.html')
            else:
                return render_template('notification.html', 
                                       notif_type='error', 
                                       title='Login Failed', 
                                       message='Invalid email or password. Please try again.', 
                                       redirect_url='/login.html')
        except Exception as e:
            return f"<h3>Database Error: {e}</h3>"
        finally:
            cursor.close()
            con.close()
    return "DB Error"

@app.route('/SendOTP', methods=['POST'])
def send_otp():
    email = request.form.get('email')
    
    # Check if email exists first
    con = get_db_connection()
    if con:
        cursor = con.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                return render_template('notification.html', 
                                       notif_type='error', 
                                       title='User Not Found', 
                                       message='This email is not registered with us.', 
                                       redirect_url='/forgot.html')
        finally:
            cursor.close()
            con.close()
            
    import random
    otp = str(random.randint(1000, 9999))
    session['otp'] = otp
    session['email'] = email
    
    # Try sending via email if configured
    smtp_user = os.getenv('SMTP_USER')
    smtp_pass = os.getenv('SMTP_PASS')
    
    if smtp_user and smtp_pass:
        try:
            import smtplib
            from email.mime.text import MIMEText
            msg = MIMEText(f"Your TripConnect verification OTP is: {otp}")
            msg['Subject'] = "TripConnect Password Reset OTP"
            msg['From'] = smtp_user
            msg['To'] = email
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
                
            return render_template('verifyOtp.html', email=email, otp_sent=True)
        except Exception as e:
            print(f"Failed to send email: {e}")
            # Fallback to demo mode if email fails
            return render_template('verifyOtp.html', email=email, demo_otp=otp)
    else:
        # Demo mode when no SMTP credentials are provided
        print(f"OTP for {email} is {otp} (Demo Mode)")
        return render_template('verifyOtp.html', email=email, demo_otp=otp)

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
                return render_template('notification.html', 
                                       notif_type='success', 
                                       title='Password Reset', 
                                       message='Your password has been updated successfully.', 
                                       redirect_url='/login.html')
            finally:
                cursor.close()
                con.close()
    else:
        return render_template('notification.html', 
                               notif_type='error', 
                               title='Verification Failed', 
                               message='The OTP you entered is invalid.', 
                               redirect_url='/forgot.html')

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
            query = "SELECT id, bus_name, from_city, to_city, travel_date, seats_available, type, arr_time, dep_time, price, image FROM buses WHERE LOWER(from_city)=LOWER(%s) AND LOWER(to_city)=LOWER(%s) AND travel_date=%s AND seats_available > 0"
            cursor.execute(query, (from_city, to_city, date))
            results = cursor.fetchall()
            for row in results:
                # 0: id, 1: name, 2: from, 3: to, 4: date, 5: seats, 6: type, 7: arr, 8: dep, 9: price, 10: image
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
                try:
                    cursor.execute(insertQuery, (fullname, mobile, bus_id, passengers))
                except mysql.connector.errors.ProgrammingError:
                    # Fallback for older schemas
                    insertQuery = "INSERT INTO busbookings (name, mobile, bus_id, passengers) VALUES (%s, %s, %s, %s)"
                    cursor.execute(insertQuery, (fullname, mobile, bus_id, passengers))
                
                updateQuery = "UPDATE buses SET seats_available = seats_available - %s WHERE id=%s AND seats_available >= %s"
                cursor.execute(updateQuery, (passengers, bus_id, passengers))
                con.commit()
                return render_template('notification.html', 
                                       notif_type='success', 
                                       title='Booking Confirmed', 
                                       message='Your bus seats have been reserved successfully.', 
                                       redirect_url='/mybooking.html')
            else:
                return render_template('notification.html', 
                                       notif_type='error', 
                                       title='Booking Failed', 
                                       message='Sorry, there are not enough seats available for this bus.', 
                                       redirect_url='/buses.html')
        except Exception as e:
             return render_template('notification.html', 
                                    notif_type='error', 
                                    title='Error', 
                                    message=f'An error occurred: {e}', 
                                    redirect_url='/buses.html')
        finally:
            cursor.close()
            con.close()
            
@app.route('/CancelBooking', methods=['POST'])
def cancel_bus_booking():
    booking_id = request.form.get('cancel_id')
    
    con = get_db_connection()
    if con:
         cursor = con.cursor()
         try:
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
            query = "SELECT id, car_name, type, price, seats, city, available, image FROM cars WHERE city=%s AND available > 0"
            cursor.execute(query, (city,))
            results = cursor.fetchall()
            for row in results:
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
             return render_template('notification.html', 
                                    notif_type='success', 
                                    title='Car Rental Confirmed', 
                                    message='Your car has been booked. Pick-up details are in your booking history.', 
                                    redirect_url='/mybooking.html')
        finally:
             cursor.close()
             con.close()
             
@app.route('/CancelCarBooking', methods=['POST'])
def cancel_car_booking():
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
             return redirect(url_for('mybooking_page'))
         finally:
             cursor.close()
             con.close()

# HOTELS

@app.route('/hotels', methods=['GET', 'POST'])
@app.route('/hotels.html', methods=['GET', 'POST'])
def hotels_page():
    if 'email' not in session:
        return redirect(url_for('login_page'))
    con = get_db_connection()
    hotels = []
    if con:
         cursor = con.cursor(dictionary=True)
         try:
              cursor.execute("SELECT name, location, price_per_night, description, image FROM hotels LIMIT 8")
              for row in cursor.fetchall():
                  hotels.append({
                      'name': row['name'],
                      'location': row['location'],
                      'price': row['price_per_night'],
                      'description': row['description'],
                      'image': row['image'] or 'https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=2670&auto=format&fit=crop'
                  })
         finally:
              cursor.close()
              con.close()
              
    selected_hotel = request.args.get('hotel', '')
    return render_template('hotels.html', hotels=hotels, selected_hotel=selected_hotel)

@app.route('/HotelSearch', methods=['POST'])
def search_hotel():
    location = request.form.get('location')
    guests = request.form.get('guests')
    
    con = get_db_connection()
    hotels = []
    if con:
         cursor = con.cursor(dictionary=True)
         try:
              q = "SELECT * FROM hotels WHERE LOWER(location) LIKE LOWER(%s) AND max_guests >= %s"
              cursor.execute(q, (f"%{location}%", guests))
              hotels = cursor.fetchall()
         finally:
              cursor.close()
              con.close()
              
    return render_template('hotels.html', hotels=hotels)

@app.route('/HotelBooking', methods=['POST'])
def hotel_booking():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    hotelName = request.form.get('hotelName')
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')
    
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
                return render_template('notification.html', 
                                       notif_type='success', 
                                       title='Hotel Room Booked', 
                                       message=f'Your stay at {hotelName} is confirmed!', 
                                       redirect_url='/mybooking.html')
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


@app.route('/create_razorpay_order', methods=['POST'])
def create_razorpay_order():
    try:
        data = request.get_json()
        if not data or 'amount' not in data:
            return jsonify({'error': 'Amount missing'}), 400
        
        amount = int(float(data['amount'])) * 100 # convert to paise
        currency = 'INR'
        
        # Create Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='1'))
        
        return jsonify({
            'order_id': razorpay_order['id'],
            'amount': amount,
            'currency': currency,
            'key_id': RAZORPAY_KEY_ID
        })
    except Exception as e:
        print(f"Razorpay Error: {e}")
        return jsonify({'error': str(e)}), 500

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
