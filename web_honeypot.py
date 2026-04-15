import sqlite3
from flask import Flask, request, render_template, redirect, session
from database import insert_attack, init_db
from datetime import timedelta
from flask import make_response

app = Flask(__name__)

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=5)
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip = request.remote_addr

        insert_attack(ip, username, password)

        return "Login Failed"
    
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "admin123":
            session.permanent = True
            session['admin'] = True
            return redirect('/dashboard')
        else:
            return "Access Denied"
        
    return render_template('admin_login.html')

    

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attacks")
    rows = cursor.fetchall()

    conn.close()

    response = make_response(render_template('dashboard.html', data=rows))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin')

def start_web():
    app.run(host='0.0.0.0', port=8080)