import os
from flask import Flask, request, redirect, render_template, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
# Use an environment variable for the secret key (with a fallback)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_default_secret_key')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# A simple user database using a dictionary
users = {'user@example.com': {'password': 'securepassword'}}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"<User {self.id}>"

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('User already exists. Please log in.', 'warning')
            return redirect(url_for('login'))
        # Add new user to the dictionary
        users[username] = {'password': password}
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')  # Ensure you have a register.html template

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')  # Ensure you have a login.html template

@app.route('/dashboard')
@login_required
def dashboard():
    # Render a dashboard template and pass current_user to the template
    return render_template('dashboard.html', user=current_user)  # Ensure you have a dashboard.html template

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
