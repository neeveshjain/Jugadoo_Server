from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.your-email.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'
app.secret_key = 'your-secret-key'
app.secret_key = "secret"
app.config["MONGO_URI"] = "mongodb+srv://info:HR5HbNCrGWoJfUFs@authentication.489yabh.mongodb.net/Authentication?retryWrites=true&w=majority&appName=Authentication"
mongo = PyMongo(app)

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)

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

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = mongo.db.users.find_one({'email': email})
        
        if user:
            token = serializer.dumps(email, salt='password-reset-salt')
            reset_url = url_for('reset_password', token=token, _external=True)
            subject = "Password Reset Requested"
            msg = Message(subject, recipients=[email])
            msg.body = f"Please click the link to reset your password: {reset_url}"
            mail.send(msg)
            flash('Password reset email sent!', 'info')
        else:
            flash('Email not found!', 'danger')
        
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        mongo.db.users.update_one({'email': email}, {'$set': {'password': hashed_password}})
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')

@app.route('/chat')
def chat():
    return render_template('chat_bot.html')

@app.route("/chat/get", methods=["GET", "POST"])
def chatting():
    msg = request.form["msg"]
    return get_Chat_response(msg)


def get_Chat_response(text):
    chat_history_ids = None
    for step in range(5):
        new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

if __name__ == '__main__':
    app.run(debug=True)