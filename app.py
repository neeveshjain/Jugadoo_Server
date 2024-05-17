from flask import Flask, render_template, request, redirect, session, url_for
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://info:<password>@authentication.489yabh.mongodb.net/?retryWrites=true&w=majority&appName=Authentication'
mongo = PyMongo(app)
csrf = CSRFProtect(app)  # Initialize CSRF protection

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Check if the email already exists in the database
        users = mongo.db.users
        existing_user = users.find_one({'email': email})

        if existing_user:
            # Email already exists
            return 'Email already exists. Please use a different email.'
        else:
            # Add new user to the database
            users.insert_one({'email': email, 'password': password})
            # Redirect to success page
            return redirect(url_for('registration_success'))

    # Render the registration template with the CSRF token
    return render_template('register.html', form=form, csrf_token=csrf_token())

@app.route('/registration_success')
def registration_success():
    return 'Registration successful!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = mongo.db.users
        login_user = users.find_one({'email': form.email.data})

        if login_user:
            if login_user['password'] == form.password.data:
                session['email'] = form.email.data
                return redirect('/')
            return 'Invalid email/password combination'
        return 'User not found!'

    return render_template('login.html', form=form, csrf_token=csrf_token())
def home():
    if 'email' in session:
        return f"Logged in as {session['email']}"
    return 'You are not logged in'

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)