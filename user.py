import os
from flask import Flask, request, redirect, render_template, url_for, flash
from flask_login import (LoginManager, UserMixin,
                         login_user, login_required,
                         logout_user, current_user)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Use an environment variable for the secret key (with a sensible default)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_default_secret_key')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# A very simple in-memory user store.  For a real application, use a database.
users = {
    'user@example.com': {
        'password': generate_password_hash('securepassword'),
        'id': 'user@example.com'
    }
}

class User(UserMixin):
    '''A minimal User class required by Flask‑Login.'''
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f'<User {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    '''Flask‑Login user loader callback.'''
    if user_id in users:
        return User(user_id)
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Register a new user (demonstration only; no persistent storage).'''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            flash('User already exists. Please log in.', 'warning')
        else:
            users[email] = {
                'password': generate_password_hash(password),
                'id': email
            }
            flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Log a user in if credentials are valid.'''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and check_password_hash(users[email]['password'], password):
            user = User(email)
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    '''A protected page accessible only to logged‑in users.'''
    return render_template('dashboard.html', user=current_user.id)

@app.route('/logout')
@login_required
def logout():
    '''Log the current user out.'''
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
