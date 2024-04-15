from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Configure Flask-Login
login_manager.login_view = 'login'

# Set the maximum inactivity time (in seconds) before auto-logout
MAX_INACTIVITY_TIME = 300  # 5 minutes

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)



# User loader function
@login_manager.user_loader
def load_user(user_id):
    # Load a user object from the database using the user ID
    return User.query.get(int(user_id))



database = [
    {"code_number": "0100", "description": "Assosiy vositalar"},
    {"code_number": "0110", "description": "Yer"},
    {"code_number": "0111", "description": "Yerni obodonlashtirish"},
    {"code_number": "0112", "description": "Moliyaviy ijara shartnomasi bo'yicha olingan asosiy vositalarni obodonlashtirish"}
]



# Middleware to check user activity and log them out if inactive for too long
@app.before_request
def before_request():
    if 'last_activity' in session:
        if 'username' in session:
            if (datetime.now() - session['last_activity']).seconds > MAX_INACTIVITY_TIME:
                flash('You have been automatically logged out due to inactivity.', 'warning')
                session.pop('username', None)
        else:
            session['last_activity'] = datetime.now()



@app.before_request
def check_session_expiry():
    if 'user_id' in session:
        last_activity = session.get('last_activity')
        if last_activity is not None:
            expiration_time = last_activity + timedelta(minutes=30)  # Session expires after 30 minutes
            if datetime.now() > expiration_time:
                # Session has expired, log the user out
                logout_user()
                session.clear()



@app.before_request
def check_ip_address_change():
    if 'user_ip' in session:
        if request.remote_addr != session['user_ip']:
            # IP address has changed unexpectedly, log the user out
            logout_user()
            session.clear()



# Routes for user authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            special_code = request.form['special_code']
            hashed_password = generate_password_hash(password)
           
            # Check if the special code is valid
            if special_code != '987234':  # Replace 'your_special_code' with your actual special code
                error = 'Invalid special code.'
                return render_template('register.html', error=error)
            
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

        except IntegrityError:
            error = 'Username or email already exists.'
            return render_template('register.html', error=error)
   
    return render_template('register.html')



# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Validate login credentials
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            session['user_id'] = user.id
            session['user_ip'] = request.remote_addr
            session['last_activity'] = datetime.now()  # Update last activity time upon login
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'
            flash('Invalid username or password', 'error')
            return render_template('login.html', error=error)    
    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/')
def landing():
    return render_template('login.html')



@app.route('/index')
@login_required
def index():
    session['last_activity'] = datetime.now()  # Update last activity time upon accessing the index page
    return render_template('index.html')



@app.route('/autophrasecomplete', methods=['GET'])
@login_required
def autophrasecomplete():
    term = request.args.get('term')
    suggestions = []

    # Query the database for matching suggestions based on the term
    for item in database:
        if term.lower() in item['description'].lower():
            suggestions.append(item['description'])
        
    return jsonify(suggestions)



@app.route('/autonumcomplete', methods=['GET'])
@login_required
def autonumcomplete():
    term = request.args.get('term')
    suggestions = []

    # Query the database for matching suggestions based on the term
    for item in database:
        if term.lower() in item['code_number'].lower():
            suggestions.append(item['description'])

    return jsonify(suggestions)



@app.route('/search', methods=['GET'])
@login_required
def search():
    code_number = request.args.get('code_number')
    phrase = request.args.get('phrase')
    results = []

    # Perform search based on code number and/or phrase
    if code_number:
        # Find an item with the exact code number
        matching_item = next((item for item in database if item['code_number'] == code_number), None)
        if matching_item:
            results.append(matching_item)
        # Also include items where the code number appears in the description
        related_items = [item for item in database if code_number in item['description']]
        results.extend(related_items)
    if phrase:
        # Filter items based on the phrase
        results.extend([item for item in database if phrase.lower() in item['description'].lower()])

    if not results:
        message = "No results found."
    else:
        message = None

    return render_template('search_results.html', results=results, message=message)



if __name__ == '__main__':
    app.run(debug=True)
