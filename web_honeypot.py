import sqlite3
from flask import Flask, request, render_template
from database import insert_attack, init_db

app = Flask(__name__)

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

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attacks")
    rows = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html', data=rows)

def start_web():
    app.run(host='0.0.0.0', port=8080)