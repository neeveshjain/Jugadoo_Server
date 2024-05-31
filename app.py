from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret"
app.config["MONGO_URI"] = "mongodb+srv://info:HR5HbNCrGWoJfUFs@authentication.489yabh.mongodb.net/Authentication?retryWrites=true&w=majority&appName=Authentication"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
            mongo.db.users.insert_one({'name' : request.form['name'], 'email' : request.form['email'], 'password' : hashed_password})
            flash('Registration Successful!')
            return redirect(url_for('index'))     
        flash('User already exists!')
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_user = mongo.db.users.find_one({'email' : request.form['email']})

        if login_user:
            if check_password_hash(login_user['password'], request.form['password']):
                flash('Logged in successfully!')
                return redirect(url_for('index'))

        flash('Invalid username/password combination')
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


if __name__ == '__main__':
    app.run(debug=True)