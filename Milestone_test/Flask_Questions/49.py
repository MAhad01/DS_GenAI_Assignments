from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'
app.config['SECRET_KEY'] = 'mysecret'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        user = mongo.db.users.find_one({"_id": user_id})
        if user:
            return User(user['username'], user['password'])
        return None

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        mongo.db.users.insert_one({'username': username, 'password': password})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username})
        if user and bcrypt.check_password_hash(user['password'], password):
            login_user(User(user['username'], user['password']))
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return 'Hello Geeks!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
