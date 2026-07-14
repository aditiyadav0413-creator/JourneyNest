# --- IMPORTS ---
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# --- APP INITIALIZATION ---
app = Flask(__name__)
CORS(app)
app.secret_key = 'your-very-secret-key-for-journeynest'

# --- HELPER FUNCTION ---
def write_to_csv(filename, data, fieldnames):
    """Writes a dictionary of data to a CSV file."""
    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# --- PAGE RENDERING ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/book')
def book():
    return render_template('book.html')
    
@app.route('/booking-page')
def booking_page():
    return render_template('booking-page.html')

@app.route('/packages')
def packages():
    return render_template('package.html')

@app.route('/services')
def services():
    return render_template('service.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
    
@app.route('/payment-page')
def payment_page():
    return render_template('payment.html')

# --- ✅ FIXED DASHBOARD ROUTE ---
# --- ✅ UPDATED DASHBOARD ROUTE ---

# --- ✅ REPLACE WITH THIS SIMPLIFIED VERSION ---
@app.route('/dashboard')
def dashboard():
    """Renders the user's dashboard if they are logged in."""
    # Protect this route: only logged-in users can see it
    if 'user_email' in session:
        # The new dashboard template gets user_name and user_email directly from the session
        # so we don't need to read any files here.
        return render_template('dashboard.html')
    else:
        # If no one is logged in, redirect them to the homepage
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear() # Clears all session data
    return redirect(url_for('index'))

# --- AUTHENTICATION & API ROUTES ---
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'message': 'All fields are required.'}), 400
    
    try:
        if os.path.exists('users.csv'):
            with open('users.csv', mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                if any(row.get('email') == email for row in reader):
                    return jsonify({'message': 'Email already registered.'}), 409
    except (FileNotFoundError, IOError):
        pass

    hashed_password = generate_password_hash(password)
    user_data = {'name': name, 'email': email, 'password': hashed_password}
    write_to_csv('users.csv', user_data, ['name', 'email', 'password'])
    
    # Automatically log the user in after registration
    session['user_email'] = email
    session['user_name'] = name
    
    return jsonify({'message': 'Registration successful!'}), 201

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400
    
    try:
        with open('users.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for user in reader:
                if user.get('email') == email and check_password_hash(user.get('password', ''), password):
                    # SUCCESS: Store user's email AND name in the session
                    session['user_email'] = user['email']
                    session['user_name'] = user['name'] 
                    return jsonify({'message': 'Login successful!'}), 200
    except (FileNotFoundError, IOError):
        return jsonify({'message': 'Invalid email or password.'}), 401
    
    return jsonify({'message': 'Invalid email or password.'}), 401

# --- ✅ FIXED: REMOVED DUPLICATE BOOKING FUNCTION ---
@app.route('/book-now', methods=['POST'])
def handle_booking():
    """Handles the main booking form submission."""
    try:
        data = {
            'from_place': request.form.get('from_place'),
            'to_place': request.form.get('to_place'),
            'guests': request.form.get('guests'),
            'arrival': request.form.get('arrival'),
            'leaving': request.form.get('leaving')
        }
        fieldnames = ['from_place', 'to_place', 'guests', 'arrival', 'leaving']
        write_to_csv('bookings.csv', data, fieldnames)
        return jsonify({'message': f"Booking from {data['from_place']} to {data['to_place']} was successful!"})
    except Exception as e:
        print(f"Error in /book-now: {e}")
        return jsonify({'message': 'Server error during booking.'}), 500



# --- ✅ ADD THIS NEW ROUTE FOR THE CONTACT FORM ---
@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Handles submission from the contact page form."""
    try:
        # 1. Get the data from the form
        contact_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('number'),
            'subject': request.form.get('subject'),
            'message': request.form.get('message'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # 2. Define the CSV file headers
        fieldnames = ['name', 'email', 'phone', 'subject', 'message', 'timestamp']

        # 3. Write the data to contacts.csv
        write_to_csv('contacts.csv', contact_data, fieldnames)
        
        # 4. Redirect back to the contact page after successful submission
        return redirect(url_for('contact'))

    except Exception as e:
        # In case of an error, print it to the terminal
        print(f"Error in /submit-contact: {e}")
        # You can also return an error response if you want
        return "An error occurred.", 500
    
# --- FORM SUBMISSION ROUTES ---
@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_details = {
        'destination': request.form.get('destination'),
        'source': request.form.get('source'),
        'date': request.form.get('date'),
        'guests': request.form.get('guests'),
        'price': request.form.get('price'),
        'cardholder_name': request.form.get('cardholder_name'),
        'payment_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_email': session.get('user_email', 'Guest') 
    }
    fieldnames = ['destination', 'source', 'date', 'guests', 'price', 'cardholder_name', 'payment_time', 'user_email']
    write_to_csv('payments.csv', payment_details, fieldnames)
    return redirect(url_for('confirmation'))

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    feedback_data = { 'name': request.form.get('reviewer_name'), 'email': request.form.get('reviewer_email'), 'rating': request.form.get('rating'), 'comments': request.form.get('comments') }
    write_to_csv('feedback.csv', feedback_data, ['name', 'email', 'rating', 'comments'])
    return redirect(url_for('review'))

# --- RUN THE APP ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))