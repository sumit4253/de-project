from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime
import requests
import os
from functools import wraps
from dotenv import load_dotenv
import database

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default-dev-secret-key')

# ==========================================
# DECORATORS & AUTH HELPERS
# ==========================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==========================================
# PUBLIC ROUTES
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        db = database.get_db()
        if db is not None:
            db.contact_messages.insert_one({
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
                'status': 'unread',
                'submitted_at': datetime.utcnow()
            })
            flash('Your message has been sent successfully!', 'success')
        else:
            flash('Database error. Please try again later.', 'danger')
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        db = database.get_db()
        if db is not None:
            # Check if exists
            if db.users.find_one({'email': email}):
                flash('Email already registered!', 'danger')
            else:
                hashed_pw = generate_password_hash(password)
                db.users.insert_one({
                    'name': name,
                    'email': email,
                    'password_hash': hashed_pw,
                    'role': 'farmer',
                    'created_at': datetime.utcnow()
                })
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
        else:
            flash('Database error. Please try again later.', 'danger')
            
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        db = database.get_db()
        if db is not None:
            user = db.users.find_one({'email': email})
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = str(user['_id'])
                session['name'] = user['name']
                session['role'] = user.get('role', 'farmer')
                flash(f'Welcome back, {user["name"]}!', 'success')
                if session['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'danger')
        else:
            flash('Database error. Please try again later.', 'danger')
            
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ==========================================
# FARMER DASHBOARD & LOGIC
# ==========================================
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/history')
@login_required
def history():
    db = database.get_db()
    records = []
    if db is not None:
        # Aggregation to mimic JOIN
        pipeline = [
            {"$match": {"user_id": ObjectId(session['user_id'])}},
            {"$lookup": {
                "from": "crops",
                "localField": "crop_id",
                "foreignField": "_id",
                "as": "crop_info"
            }},
            {"$unwind": {"path": "$crop_info", "preserveNullAndEmptyArrays": True}},
            {"$sort": {"calculation_date": -1}}
        ]
        
        raw_records = list(db.calculations.aggregate(pipeline))
        for row in raw_records:
            # Flatten for template compatibility
            row['crop_name'] = row.get('crop_info', {}).get('name', 'Auto Fallback')
            records.append(row)
            
    return render_template('history.html', records=records)

@app.route('/api/weather', methods=['POST'])
@login_required
def get_weather():
    data = request.get_json()
    city = data.get('city')
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    
    if not api_key or api_key == 'your_openweathermap_api_key_here':
        return jsonify({
            'success': True,
            'data': {
                'temp': 28.5, 'humidity': 65, 'pressure': 1012,
                'wind_speed': 4.5, 'clouds': 20, 'rain_prob': 10,
                'description': 'clear sky (dummy)'
            },
            'warning': 'Using dummy data. Provide API key for real data.'
        })
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        res = response.json()
        return jsonify({
            'success': True,
            'data': {
                'temp': res['main']['temp'],
                'humidity': res['main']['humidity'],
                'pressure': res['main']['pressure'],
                'wind_speed': res.get('wind', {}).get('speed', 0),
                'clouds': res.get('clouds', {}).get('all', 0),
                'rain_prob': 0,
                'description': res['weather'][0]['description']
            }
        })
    return jsonify({'success': False, 'message': 'City not found or API error.'})

@app.route('/api/calculate', methods=['POST'])
@login_required
def calculate():
    data = request.get_json()
    city = data.get('city')
    farm_size = float(data.get('farm_size', 0))
    soil_moisture = float(data.get('soil_moisture', 0))
    temp = float(data.get('temperature', 0))
    humidity = float(data.get('humidity', 0))
    
    db = database.get_db()
    recommended_crops = []
    water_req = 0
    crop_id = None
    
    if db is not None:
        # Recommend crops based on temp and humidity
        cursor = db.crops.find({
            'min_temp': {'$lte': temp},
            'max_temp': {'$gte': temp},
            'min_humidity': {'$lte': humidity},
            'max_humidity': {'$gte': humidity}
        })
        # Convert cursor to list and ObjectId to string for JSON serialization
        for crop in cursor:
            crop['_id'] = str(crop['_id'])
            recommended_crops.append(crop)
        
        if recommended_crops:
            best_crop = recommended_crops[0]
            crop_id = ObjectId(best_crop['_id'])
            temp_factor = max(1, temp / 25)
            soil_factor = max(0, (100 - soil_moisture) / 100)
            water_req = best_crop['base_water_req'] * farm_size * temp_factor * soil_factor
        else:
            water_req = 5 * farm_size * (temp/20) * ((100-soil_moisture)/100)
            
        water_req = round(water_req, 2)
        
        # Save to history
        db.calculations.insert_one({
            'user_id': ObjectId(session['user_id']),
            'city': city,
            'farm_size': farm_size,
            'crop_id': crop_id,
            'temperature': temp,
            'humidity': humidity,
            'soil_moisture': soil_moisture,
            'water_required': water_req,
            'calculation_date': datetime.utcnow()
        })
        
    return jsonify({
        'success': True,
        'water_required': water_req,
        'recommended_crops': recommended_crops,
        'efficiency_tips': "Water during early morning or late evening to minimize evaporation."
    })

# ==========================================
# ADMIN ROUTES
# ==========================================
@app.route('/admin')
@admin_required
def admin_dashboard():
    stats = {}
    db = database.get_db()
    if db is not None:
        stats['users'] = db.users.count_documents({'role': 'farmer'})
        stats['crops'] = db.crops.count_documents({})
        stats['calculations'] = db.calculations.count_documents({})
    return render_template('admin_dashboard.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
