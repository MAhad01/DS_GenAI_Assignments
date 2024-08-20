from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {'admin': 'password'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return 'Login Page'

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome {session['username']}!"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
